import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal, Base, engine
from app.models.student import Student
from app.models.drive import Drive, InterviewSlot
from app.services.readiness import evaluate_readiness

# Recreate tables to ensure schema matches model definitions perfectly
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

BRANCHES = ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil"]
SKILLS = ["Python", "Java", "C++", "React", "Node.js", "SQL", "Docker", "AWS", "FastAPI", "MongoDB"]
NAMES = ["Aarav Sharma", "Pooja Nayak", "Rohan Rath", "Sneha Panda", "Vikram Patel", "Ananya Mohapatra"]

def seed():
    # 1. Clean existing records
    db.query(Student).delete()
    db.query(Drive).delete()
    db.commit()

    # 2. Add students
    students = []
    for i in range(150):
        cgpa = round(random.uniform(5.5, 9.8), 2)
        mock = round(random.uniform(35.0, 95.0), 1)
        selected_skills = random.sample(SKILLS, k=random.randint(2, 5))
        score, band = evaluate_readiness(cgpa, mock, len(selected_skills))

        student = Student(
            name=f"{random.choice(NAMES)} {i}",
            email=f"candidate_{i}@bput.ac.in",
            branch=random.choice(BRANCHES),
            cgpa=cgpa,
            skills=selected_skills,
            mock_score=mock,
            readiness_band=band,
            readiness_score=score
        )
        students.append(student)

    # Use add_all instead of bulk_save_objects for proper JSON serialization in SQLite
    db.add_all(students)
    db.commit()

    # 3. Add drives
    drives = [
        Drive(
            company_name="TCS Digital",
            role_title="Systems Engineer",
            min_cgpa=7.0,
            min_mock_score=65.0,
            target_branches=["CSE", "IT", "ECE"],
            required_skills=["Java", "SQL", "Python"]
        ),
        Drive(
            company_name="CloudNine Tech",
            role_title="Cloud & DevOps Engineer",
            min_cgpa=7.5,
            min_mock_score=75.0,
            target_branches=["CSE", "IT"],
            required_skills=["Docker", "AWS", "Python", "FastAPI"]
        )
    ]
    db.add_all(drives)
    db.commit()
    print("Database seeded successfully with mock candidates and company drives!")

if __name__ == "__main__":
    seed()
    db.close()