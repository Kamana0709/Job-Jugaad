from datetime import datetime
from sqlalchemy.orm import Session
from app.models.drive import InterviewSlot

def detect_scheduling_conflict(
    db: Session,
    student_id: int,
    start_time: datetime,
    end_time: datetime,
    interviewer_id: str = None
) -> dict:
    if start_time >= end_time:
        return {
            "has_conflict": True,
            "conflict_type": "INVALID_TIME",
            "message": "Start time must occur before end time."
        }

    # Condition: StartA < EndB and EndA > StartB
    student_clash = db.query(InterviewSlot).filter(
        InterviewSlot.student_id == student_id,
        InterviewSlot.status != "CANCELLED",
        InterviewSlot.start_time < end_time,
        InterviewSlot.end_time > start_time
    ).first()

    if student_clash:
        return {
            "has_conflict": True,
            "conflict_type": "STUDENT_OVERLAP",
            "conflicting_id": student_clash.id,
            "message": f"Student is already booked from {student_clash.start_time.strftime('%H:%M')} to {student_clash.end_time.strftime('%H:%M')}."
        }

    if interviewer_id:
        interviewer_clash = db.query(InterviewSlot).filter(
            InterviewSlot.interviewer_id == interviewer_id,
            InterviewSlot.status != "CANCELLED",
            InterviewSlot.start_time < end_time,
            InterviewSlot.end_time > start_time
        ).first()

        if interviewer_clash:
            return {
                "has_conflict": True,
                "conflict_type": "INTERVIEWER_OVERLAP",
                "conflicting_id": interviewer_clash.id,
                "message": "Interviewer is assigned to another interview slot during this period."
            }

    return {"has_conflict": False, "message": "Slot is available."}