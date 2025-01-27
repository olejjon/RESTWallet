from sqlalchemy import Column, String, Float
from .database import Base

class Wallet(Base):
    __tablename__ = "wallets"
    uuid = Column(String, primary_key=True, index=True)
    balance = Column(Float, default=0.0)