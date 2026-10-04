from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    drive_id = Column(Integer, ForeignKey("drives.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    interviewer_id = Column(String, nullable=True)
    status = Column(String, default="SCHEDULED")  # SCHEDULED, COMPLETED, CANCELLED

    student = relationship("Student", back_populates="interviews")
    drive = relationship("Drive", back_populates="interviews")