from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# OWNER TABLE
class Owner(Base):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    address = Column(String)

    pets = relationship("Patient", back_populates="owner")


# PATIENT TABLE
class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    species = Column(String)
    breed = Column(String)
    age = Column(String)
    sex = Column(String)
    weight = Column(String)

    owner_id = Column(Integer, ForeignKey('owners.id'))

    owner = relationship("Owner", back_populates="pets")
    histories = relationship("MedicalHistory", back_populates="patient")


# MEDICAL HISTORY TABLE
class MedicalHistory(Base):
    __tablename__ = 'histories'
    id = Column(Integer, primary_key=True)

    # Vitals
    weight = Column(String)
    temperature = Column(String)
    heart_rate = Column(String)
    respiratory_rate = Column(String)

    # FAS (Fear, Anxiety, Stress)
    fas_score = Column(String)
    fas_notes = Column(Text)

    # General history
    medications = Column(Text)
    allergies = Column(Text)
    past_history = Column(Text)
    diet = Column(Text)
    reason = Column(Text)
    notes = Column(Text)

    # Reproductive status
    reproductive_status = Column(String)

    # Vaccines (store as text for now)
    vaccines = Column(Text)

    # Physical exam sections
    integument = Column(Text)
    ent = Column(Text)
    msk = Column(Text)
    lymph_nodes = Column(Text)
    cardiovascular = Column(Text)
    respiratory = Column(Text)
    gastrointestinal = Column(Text)
    neurologic = Column(Text)

    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship("Patient", back_populates="histories")

from datetime import datetime
date = Column(String, default=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))


# DATABASE SETUP
engine = create_engine('sqlite:///vet_records.db')
Session = sessionmaker(bind=engine)