import sqlalchemy as db
from app import engine, Base
from sqlalchemy import Column, Float, String, Integer, TIMESTAMP
import datetime
import pytz


tokyo = pytz.timezone('Asia/Tokyo')

class transaction(Base):
    __tablename__ = 'Transaction'
    id = Column(String(100), primary_key=True)
    created_at = Column(TIMESTAMP,default=tokyo.localize(datetime.datetime.now()))
    updated_at = Column(TIMESTAMP,default=tokyo.localize(datetime.datetime.now()))
    expired_at = Column(TIMESTAMP,default=tokyo.localize(datetime.datetime.now()))
    transaction_id = Column(String(255),nullable=False)
    account = Column(String(255),nullable=False)
    payment_method = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    point = Column(Float, nullable=False)
    transaction_status = Column(String(255),nullable=False)

Base.metadata.create_all(engine, checkfirst=True)
