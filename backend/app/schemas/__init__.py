from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    branch: str
    cgpa: float
    skills: List[str]
    mock_interview_score: float = 0.0

class DriveCreate(BaseModel):
    company_name: str
    role_title: str
    min_cgpa: float
    required_skills: List[str]
    min_mock_score: float = 65.0
    package_lpa: float = 6.5

class SlotScheduleRequest(BaseModel):
    drive_id: int
    student_id: int
    start_time: datetime
    end_time: datetime
    interviewer_name: Optional[str] = "Tech Panel 1"