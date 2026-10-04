from typing import List, Dict

def evaluate_readiness(cgpa: float, mock_score: float, skill_count: int) -> tuple[float, str]:
    cgpa_norm = min(max((cgpa / 10.0) * 100, 0), 100)
    skill_norm = min((skill_count / 8.0) * 100, 100)
    score = round((0.4 * cgpa_norm) + (0.4 * mock_score) + (0.2 * skill_norm), 1)

    if score >= 80:
        band = "Highly Employable"
    elif score >= 65:
        band = "Ready"
    elif score >= 45:
        band = "Developing"
    else:
        band = "Not Ready"

    return score, band

def detect_skill_gaps(student_skills: List[str], target_skills: List[str]) -> Dict[str, List[str]]:
    student_set = set(s.strip().lower() for s in student_skills)
    target_set = set(s.strip().lower() for s in target_skills)

    return {
        "matched": list(student_set.intersection(target_set)),
        "missing": list(target_set.difference(student_set))
    }