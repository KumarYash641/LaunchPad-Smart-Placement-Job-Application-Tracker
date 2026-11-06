from django.test import TestCase
from django.contrib.auth.models import User
from tracker.models import StudentProfile, Company, Job
from tracker.services import check_eligibility


class EligibilityTests(TestCase):
    def test_student_meets_cgpa_and_skill_requirements(self):
        user = User.objects.create_user(username="student", password="test-pass-123")
        profile = user.student_profile
        profile.cgpa = 8.0
        profile.skills = "Python, SQL"
        profile.save()
        company = Company.objects.create(name="Example Tech")
        job = Job.objects.create(
            title="Python Developer",
            company=company,
            description="Build software.",
            min_cgpa=7.0,
            required_skills="Python, SQL",
        )
        eligible, reasons = check_eligibility(profile, job)
        self.assertTrue(eligible)
        self.assertEqual(reasons, [])
