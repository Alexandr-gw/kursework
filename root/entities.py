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
    username = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    birthdate = Column(TIMESTAMP, nullable=False)
    sex = Column(String, nullable=False)


class Symptom(Base):
    __tablename__ = 'symptom'
    symptom_name = Column(String, primary_key=True)
    drug = relationship("Drug", cascade="all, delete", passive_deletes=True)


class Contraindication(Base):
    name = Column(String, primary_key=True)
    additional_info = Column(String, nullable=True)
    drug = relationship("Drug", cascade="all, delete", passive_deletes=True)


class Drug(Base):
    drug_name = Column(String, primary_key=True)
    price = Column(Float, nullable=False)
    symptom_name = Column(String, ForeignKey(Symptom.symptom_name, ondelete="cascade"), primary_key=True)
    contraindication = Column(String, ForeignKey(Contraindication.name, ondelete="cascade"), primary_key=True)
