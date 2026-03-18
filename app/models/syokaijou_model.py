import sqlalchemy as db
from app import engine, Base
from sqlalchemy import Column, Float, String, TIMESTAMP, Text
import datetime
import pytz


tokyo = pytz.timezone('Asia/Tokyo')

class syokaijou(Base):
    __tablename__ = 'Syokaijou'
    id = Column(String(100), primary_key=True)
    created_at = Column(TIMESTAMP,default=tokyo.localize(datetime.datetime.now()))
    updated_at = Column(TIMESTAMP,default=tokyo.localize(datetime.datetime.now()))
    username = Column(String(255),nullable=False)
    date = Column(String(255), nullable=False)
    disease_name = Column(String(255), nullable=False)
    introduction_purpose = Column(String(255), nullable=False)
    summary = Column(Text,nullable=False)
    file_location = Column(Text,nullable=False)

Base.metadata.create_all(engine, checkfirst=True)
