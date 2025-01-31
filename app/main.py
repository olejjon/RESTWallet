from redis import Redis
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .models import Wallet
from .schemas import OperationRequest, WalletResponse, WalletCreateRequest
from .config import settings

app = FastAPI()

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

@app.post("/api/v1/wallets/{wallet_uuid}/operation")
async def perform_operation(wallet_uuid: str, operation: OperationRequest,
                            db: AsyncSession = Depends(get_db)):
    async with db.begin():
        wallet = await db.execute(select(Wallet).filter(Wallet.uuid == wallet_uuid).with_for_update())
        wallet = wallet.scalars().first()
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        if operation.operationType == "DEPOSIT":
            wallet.balance += operation.amount
        elif operation.operationType == "WITHDRAW":
            if wallet.balance < operation.amount:
                raise HTTPException(status_code=400, detail="Insufficient funds")
            wallet.balance -= operation.amount
        else:
            raise HTTPException(status_code=400, detail="Invalid operation type")

        await db.commit()
        redis.set(wallet_uuid, wallet.balance)
        return {"message": "Operation successful"}


@app.post("/api/v1/wallets")
async def create_wallet(wallet: WalletCreateRequest, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        existing_wallet = await db.execute(select(Wallet).filter(Wallet.uuid == wallet.uuid))
        existing_wallet = existing_wallet.scalars().first()
        if existing_wallet:
            raise HTTPException(status_code=400, detail="Wallet already exists")

        new_wallet = Wallet(uuid=wallet.uuid, balance=wallet.balance)
        db.add(new_wallet)
        await db.commit()

    async with db.begin():
        await db.refresh(new_wallet)
        redis.set(wallet.uuid, new_wallet.balance)
        return {"message": "Wallet created successfully", "wallet": new_wallet}


@app.get("/api/v1/wallets/{wallet_uuid}", response_model=WalletResponse)
async def get_wallet(wallet_uuid: str, db: AsyncSession = Depends(get_db)):
    balance = redis.get(wallet_uuid)
    if balance:
        return {"uuid": wallet_uuid, "balance": float(balance)}

    wallet = await db.execute(select(Wallet).filter(Wallet.uuid == wallet_uuid))
    wallet = wallet.scalars().first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    redis.set(wallet_uuid, wallet.balance)
    return wallet
