from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StudentCreate(BaseModel):
    name: str
    email: str
    branch: str
    cgpa: float
    skills: List[str] = []
    mock_score: float = 0.0

class StudentResponse(StudentCreate):
    id: int
    college_id: str
    readiness_band: str
    readiness_score: float

    class Config:
        from_attributes = True

class DriveCreate(BaseModel):
    company_name: str
    role_title: str
    min_cgpa: float = 6.0
    min_mock_score: float = 60.0
    target_branches: List[str] = []
    required_skills: List[str] = []

class DriveResponse(DriveCreate):
    id: int
    college_id: str

    class Config:
        from_attributes = True

class MatchBreakdown(BaseModel):
    cgpa_contribution: float
    skill_contribution: float
    mock_contribution: float
    matched_skills: List[str]
    missing_skills: List[str]

class MatchResult(BaseModel):
    student_id: int
    name: str
    cgpa: float
    match_score: float
    readiness_band: str
    breakdown: MatchBreakdown
    explanation: str

class SlotScheduleRequest(BaseModel):
    student_id: int
    drive_id: int
    start_time: datetime
    end_time: datetime
    interviewer_id: Optional[str] = None

class ConflictResponse(BaseModel):
    has_conflict: bool
    conflict_type: Optional[str] = None
    conflicting_id: Optional[int] = None
    message: str