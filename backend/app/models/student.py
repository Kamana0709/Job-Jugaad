from sqlalchemy import Column, Integer, String, Float, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(String, index=True, default="BPUT_001")
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    branch = Column(String, index=True)
    cgpa = Column(Float, nullable=False)
    skills = Column(JSON, default=list)
    mock_score = Column(Float, default=0.0)
    readiness_band = Column(String, default="Developing")
    readiness_score = Column(Float, default=0.0)

    interviews = relationship("InterviewSlot", back_populates="student")