from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student
from app.schemas.schemas import StudentResponse
from app.services.readiness import detect_skill_gaps

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/{student_id}", response_model=StudentResponse)
def get_student_profile(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/{student_id}/skill-gap")
def get_student_skill_gap(student_id: int, target_skills: list[str], db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    gaps = detect_skill_gaps(student.skills or [], target_skills)
    return {"student_id": student.id, "readiness_band": student.readiness_band, **gaps}
    @router.get("/", response_model=list[StudentResponse])
def list_students(limit: int = 50, skip: int = 0, db: Session = Depends(get_db)):
    return db.query(Student).offset(skip).limit(limit).all()