from typing import Dict, Any

def compute_readiness_band(score: float) -> str:
    if score >= 80:
        return "Highly Employable"
    elif score >= 65:
        return "Ready"
    elif score >= 45:
        return "Developing"
    return "Not Ready"

def evaluate_candidate_match(student, drive) -> Dict[str, Any]:
    student_skills_set = set(s.strip().lower() for s in (student.skills or []))
    required_skills_set = set(s.strip().lower() for s in (drive.required_skills or []))

    matched = list(student_skills_set.intersection(required_skills_set))
    missing = list(required_skills_set.difference(student_skills_set))

    skill_ratio = len(matched) / len(required_skills_set) if required_skills_set else 1.0
    skill_score = skill_ratio * 50.0

    cgpa_eligible = student.cgpa >= drive.min_cgpa
    cgpa_score = (min(student.cgpa / 10.0, 1.0) * 30.0) if cgpa_eligible else (min(student.cgpa / drive.min_cgpa, 1.0) * 15.0)

    mock_eligible = student.mock_score >= drive.min_mock_score
    mock_score_contrib = (min(student.mock_score / 100.0, 1.0) * 20.0)

    total_match = round(skill_score + cgpa_score + mock_score_contrib, 1)

    # Explainability generation
    notes = []
    if cgpa_eligible:
        notes.append(f"CGPA meets eligibility criteria ({student.cgpa} >= {drive.min_cgpa})")
    else:
        notes.append(f"CGPA is below minimum threshold ({student.cgpa} < {drive.min_cgpa})")

    if missing:
        notes.append(f"skill set shows a gap in {', '.join(missing[:3])}")
    else:
        notes.append("technical skills fully match requirements")

    if not mock_eligible:
        notes.append(f"mock-interview score ({student.mock_score}) is below expected benchmark ({drive.min_mock_score})")

    status_tag = "Above Threshold" if total_match >= 70 else "Below Threshold"
    explanation = f"{status_tag}: " + "; ".join(notes) + "."

    return {
        "student_id": student.id,
        "name": student.name,
        "cgpa": student.cgpa,
        "match_score": total_match,
        "readiness_band": student.readiness_band,
        "breakdown": {
            "cgpa_contribution": round(cgpa_score, 1),
            "skill_contribution": round(skill_score, 1),
            "mock_contribution": round(mock_score_contrib, 1),
            "matched_skills": matched,
            "missing_skills": missing
        },
        "explanation": explanation
    }

# Alias for compatibility
calculate_explainable_match = evaluate_candidate_match