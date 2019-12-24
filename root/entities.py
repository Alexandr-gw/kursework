from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import relationship

Base = declarative_base()


class Doctor(Base):
    __tablename__ = "doctor"
    doctor_username = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)


class Patient(Base):
    __tablename__ = "doctor"
