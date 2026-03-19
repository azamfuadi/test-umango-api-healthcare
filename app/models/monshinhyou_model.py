import sqlalchemy as db
from app import engine, Base
from sqlalchemy import Column, Float, String, TIMESTAMP, Text
import datetime
import pytz


tokyo = pytz.timezone('Asia/Tokyo')

class monshinhyou(Base):
    __tablename__ = 'Monshinhyou'
    id = Column(String(100), primary_key=True)
    created_at = Column(TIMESTAMP,default=tokyo.localize(datetime.datetime.now()))
    updated_at = Column(TIMESTAMP,default=tokyo.localize(datetime.datetime.now()))
    username = Column(String(50),nullable=False)
    date = Column(String(50), nullable=False)
    patient_name = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)
    birthday = Column(String(100),nullable=False)
    symptoms = Column(Text,nullable=False)
    current_illness = Column(Text,nullable=False)
    medication = Column(String(255),nullable=False)
    food_allergies = Column(String(255),nullable=False)
    drug_allergies = Column(String(255),nullable=False)
    medical_history = Column(Text,nullable=False)
    drinking_habits = Column(String(50),nullable=False)
    smoking_habits = Column(String(50),nullable=False)
    file_location = Column(Text,nullable=False)
    file_url = Column(Text,nullable=True)

Base.metadata.create_all(engine, checkfirst=True)
