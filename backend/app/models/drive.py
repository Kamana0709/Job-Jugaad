from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Drive(Base):
    __tablename__ = "drives"

    id = Column(Integer, primary_key=True, index=True)
    college_id = Column(String, index=True, default="BPUT_001")
    company_name = Column(String, nullable=False)
    role_title = Column(String, nullable=False)
    min_cgpa = Column(Float, default=6.0)
    min_mock_score = Column(Float, default=60.0)
    target_branches = Column(JSON, default=list)
    required_skills = Column(JSON, default=list)

    interviews = relationship("InterviewSlot", back_populates="drive")


class InterviewSlot(Base):
    __tablename__ = "interview_slots"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    drive_id = Column(Integer, ForeignKey("drives.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    interviewer_id = Column(String, nullable=True)
    status = Column(String, default="CONFIRMED")

    student = relationship("Student", back_populates="interviews")
    drive = relationship("Drive", back_populates="interviews")