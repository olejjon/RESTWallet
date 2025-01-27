from pydantic import BaseModel

class OperationRequest(BaseModel):
    operationType: str
    amount: float

class WalletResponse(BaseModel):
    uuid: str
    balance: float

class WalletCreateRequest(BaseModel):
    uuid: str
    balance: float = 0.0

