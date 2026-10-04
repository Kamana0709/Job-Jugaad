from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student
from app.models.drive import Drive
from app.schemas.schemas import DriveCreate, DriveResponse, MatchResult
from app.services.matching import evaluate_candidate_match

router = APIRouter(prefix="/api/recruiters", tags=["Recruiter"])

@router.post("/drives", response_model=DriveResponse)
def create_drive(payload: DriveCreate, db: Session = Depends(get_db)):
    drive = Drive(**payload.model_dump())
    db.add(drive)
    db.commit()
    db.refresh(drive)
    return drive

@router.get("/drives/{drive_id}/rankings", response_model=list[MatchResult])
def rank_candidates_for_drive(drive_id: int, limit: int = 50, db: Session = Depends(get_db)):
    drive = db.query(Drive).filter(Drive.id == drive_id).first()
    if not drive:
        raise HTTPException(status_code=404, detail="Drive not found")

    students = db.query(Student).all()
    results = [evaluate_candidate_match(s, drive) for s in students]
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results[:limit]
    @router.get("/drives", response_model=list[DriveResponse])
def list_drives(db: Session = Depends(get_db)):
    return db.query(Drive).all()