from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student
from app.models.drive import Drive, InterviewSlot
from app.schemas.schemas import SlotScheduleRequest, ConflictResponse, StudentResponse
from app.services.conflict import detect_scheduling_conflict

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.post("/schedule", response_model=dict)
def schedule_slot(payload: SlotScheduleRequest, db: Session = Depends(get_db)):
    """
    Checks for interview collisions before confirming a slot.
    Returns 409 Conflict if candidate or interviewer is double-booked.
    """
    conflict = detect_scheduling_conflict(
        db=db,
        student_id=payload.student_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        interviewer_id=payload.interviewer_id
    )

    if conflict.get("has_conflict"):
        raise HTTPException(status_code=409, detail=conflict)

    new_slot = InterviewSlot(
        student_id=payload.student_id,
        drive_id=payload.drive_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        interviewer_id=payload.interviewer_id,
        status="CONFIRMED"
    )
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    return {"message": "Slot scheduled successfully", "slot_id": new_slot.id}


@router.get("/at-risk-students", response_model=list[StudentResponse])
def get_at_risk_students(db: Session = Depends(get_db)):
    """
    Returns students who have low CGPA (< 6.0) or are flagged as 'Not Ready'.
    """
    return db.query(Student).filter(
        (Student.readiness_band == "Not Ready") | (Student.cgpa < 6.0)
    ).all()


@router.get("/metrics")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    """
    Returns high-level placement health stats for the Admin dashboard.
    """
    total_students = db.query(Student).count()
    at_risk_count = db.query(Student).filter(
        (Student.readiness_band == "Not Ready") | (Student.cgpa < 6.0)
    ).count()
    ready_count = db.query(Student).filter(
        Student.readiness_band.in_(["Ready", "Highly Employable"])
    ).count()
    active_drives = db.query(Drive).count()
    total_slots = db.query(InterviewSlot).count()

    return {
        "total_students": total_students,
        "ready_students": ready_count,
        "at_risk_students": at_risk_count,
        "active_drives": active_drives,
        "interviews_scheduled": total_slots
    }