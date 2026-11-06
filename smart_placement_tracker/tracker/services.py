from .models import StudentProfile


def check_eligibility(student_profile: StudentProfile, job):
    """Return (eligible, reasons) based on CGPA and required skills."""
    reasons = []
    if student_profile.cgpa < job.min_cgpa:
        reasons.append(f"Your CGPA ({student_profile.cgpa}) is below the required {job.min_cgpa}.")

    student_skills = set(student_profile.skill_list())
    required_skills = set(job.required_skill_list())
    missing_skills = sorted(required_skills - student_skills)

    if missing_skills:
        reasons.append("Missing skills: " + ", ".join(missing_skills))

    if not job.is_open():
        reasons.append("This job is closed or its application deadline has passed.")

    return len(reasons) == 0, reasons
