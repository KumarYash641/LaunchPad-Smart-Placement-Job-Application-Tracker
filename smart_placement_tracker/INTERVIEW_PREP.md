# 🎯 LaunchPad: Placement Tracker — Interview Preparation Guide

This guide is designed for quick, confident review before your interview. It breaks down technical concepts into simple language so you can explain your project clearly and impress the interviewers.

---

## 📌 1. The 60-Second Elevator Pitch

> *"LaunchPad is a full-stack campus placement and job tracking platform built with Python, Django, and Django REST Framework. It solves the chaos of manual campus recruitment by providing students with a centralized dashboard to track applications and check their eligibility for jobs in real time.*
>
> *From an engineering perspective, I focused on clean architecture: I decoupled the business logic into a dedicated **eligibility service layer**, enforced database-level **unique constraints** to prevent duplicate applications, optimized SQL queries using **`select_related`** to avoid the N+1 problem, and exposed **RESTful APIs** for integration."*

---

## 🏗️ 2. Project Architecture (How It All Connects)

```
User (Browser / API Client)
       │
       ▼
 placement_project/urls.py (Traffic Router)
       │
   ┌───┴────────────────────────┐
   ▼                            ▼
tracker/urls.py (Web Views)   tracker/api_urls.py (DRF Endpoints)
   │                            │
tracker/views.py              tracker/api_views.py
   │                            │
   ├──> tracker/forms.py        ├──> tracker/serializers.py
   ├──> tracker/services.py     │
   │    (Eligibility Check)     │
   ▼                            ▼
tracker/models.py (Database: User, StudentProfile, Company, Job, Application)
   │
   ▼
SQLite (Development) / MySQL (Production via .env)
```

### Key Files & What They Do:
1. **`tracker/models.py`**: Defines the database schema: `Company`, `Job`, `StudentProfile`, and `Application`.
2. **`tracker/services.py`**: Contains pure business logic (eligibility calculation) separated from HTTP requests.
3. **`tracker/views.py`**: Handles web page rendering, user login, and form submissions.
4. **`tracker/api_views.py` & `serializers.py`**: Converts database models into JSON for REST endpoints.
5. **`tracker/signals.py`**: Automatically creates a `StudentProfile` whenever a new `User` is registered.

---

## 💡 3. Core Technical Concepts (Explained Simply)

### A. The N+1 Query Problem & `select_related`
* **What is N+1?** If you have 20 applications and query `Application.objects.all()`, then loop through them in a template saying `{{ app.job.company.name }}`, Django makes:
  * 1 query for all applications
  * 20 extra queries to fetch each job and company
  * Total = 21 queries (slow!).
* **How you solved it:** Using `Application.objects.select_related("job", "job__company")`.
* **How it works:** It performs an SQL `INNER JOIN` in a **single query**, fetching applications, jobs, and companies all at once.

### B. Duplicate Application Protection (Race Condition Prevention)
* **The Problem:** If a user clicks "Apply" twice rapidly, two separate requests could create duplicate rows in the database.
* **The Solution:** Added a database-level constraint in `tracker/models.py`:
  ```python
  UniqueConstraint(fields=["student", "job"], name="unique_student_job_application")
  ```
* In `tracker/views.py`, caught `IntegrityError` so if a duplicate happens, the user gets a friendly warning message instead of a 500 error page.

### C. Decoupled Service Layer (`services.py`)
* **Why not put eligibility check inside `views.py`?**
  * Views should only handle HTTP requests and responses.
  * Moving business logic into `services.py` makes it **testable with unit tests**, reusable across both web views and REST APIs, and adheres to the **Single Responsibility Principle**.

### D. Signals (`post_save`)
* When a student registers, Django triggers a `post_save` signal from `tracker/signals.py`.
* This ensures every registered `User` automatically has a corresponding `StudentProfile` without messy conditional checks across the codebase.

### E. Environment Configuration (`python-dotenv`)
* Hardcoded secrets and passwords in code are security risks.
* You used `.env` loaded via `load_dotenv()` in `settings.py`. This allows seamless switching between **SQLite for local development** and **MySQL for production** by changing just one variable (`DB_ENGINE=mysql`).

---

## ❓ 4. Top 10 Interview Questions & Answers

### Q1: "Why did you build this project?"
> *"Campus placement season is often chaotic, with job requirements scattered across emails, spreadsheets, and messaging groups. Students often waste time applying to jobs they don't qualify for. I built LaunchPad to give students automated eligibility verification and a clean status dashboard, while giving placement coordinators a central hub to review applicants."*

### Q2: "Can you explain the database relationships?"
> *"There are four main models:
> 1. `User` has a **One-to-One** relationship with `StudentProfile`.
> 2. `Company` has a **One-to-Many** relationship with `Job` (one company, multiple job postings).
> 3. `Job` and `User` connect through `Application` as a **Many-to-Many** intermediary table (a student can apply to many jobs, and a job can have many applicants).*
> *I also added a composite `UniqueConstraint` on `(student, job)` to strictly enforce that a student can only apply once per job."*

### Q3: "How does the eligibility checker work?"
> *"It lives in `tracker/services.py` inside the function `check_eligibility(student_profile, job)`. It performs three checks:
> 1. **CGPA Check:** Checks if `profile.cgpa >= job.min_cgpa`.
> 2. **Skills Matching:** Compares lowercase, stripped sets of the student's skills against required skills using Python `set` operations (`required_skills - student_skills`). Any missing skills are collected.
> 3. **Deadline Check:** Verifies if the job is active and the deadline hasn't passed against `timezone.localdate()`.
> It returns a tuple: `(is_eligible: bool, reasons: list)`."*

### Q4: "Why use both Django Template Views and Django REST Framework?"
> *"I implemented a hybrid architecture:
> - **Django Templates:** For rapid server-side rendered (SSR) pages that are SEO-friendly and have built-in CSRF protection.
> - **DRF APIs:** To decouple the backend and allow future mobile apps or third-party integrations (like a college mobile app) to query available jobs and user application statuses via JSON."*

### Q5: "How did you handle authentication and security?"
> *"1. **Authentication:** Used Django's built-in session authentication and `UserCreationForm` with salted PBKDF2 password hashing.
> 2. **Authorization:** Used `@login_required` on student views and `@user_passes_test(lambda u: u.is_staff)` on administrative/staff views so students cannot access management screens.
> 3. **CSRF:** Added `{% csrf_token %}` to all POST forms to prevent Cross-Site Request Forgery.
> 4. **XSS & SQL Injection:** Django's ORM uses parameterized queries (preventing SQL injection), and templates auto-escape HTML output (preventing XSS)."*

### Q6: "What is the difference between `forms.py` and `serializers.py`?"
> *"`forms.py` validates input coming from HTML web forms (`POST` request data) and renders HTML widgets. `serializers.py` in DRF validates and transforms complex Python model instances into JSON data (and vice-versa) for API endpoints."*

### Q7: "What was a tricky bug you found and fixed in this project?"
> *"Two key ones:
> 1. In the student profile view, the profile retrieval had an unpacking bug that caused a 500 error if a user profile didn't exist yet. I replaced it with `StudentProfile.objects.get_or_create(...)` to guarantee the profile always exists safely.
> 2. In the REST API search filter, combining two filtered QuerySets with the `|` operator was creating duplicate rows. I refactored it to use Django's `Q` objects (`Q(title__icontains=search) | Q(company__name__icontains=search)`), which translates cleanly into a single SQL `WHERE ... OR ...` clause."*

### Q8: "How would you scale this app to handle 100,000 students?"
> *"1. **Database:** Migrate from SQLite to PostgreSQL or MySQL with connection pooling (PgBouncer) and add database indexes on frequently filtered fields like `Job.is_active` and `Application.status`.
> 2. **Caching:** Cache frequently accessed static listings like `/api/jobs/` using Redis so we don't hit the database on every page load.
> 3. **Background Tasks:** Offload slow operations like sending confirmation emails to a Celery task queue with a Redis message broker.
> 4. **Static Assets:** Serve static and media files via Amazon S3 / CloudFront CDN rather than through the web server."*

### Q9: "Why did you use SQLite locally instead of MySQL directly?"
> *"SQLite is zero-configuration and file-based, making development and automated CI testing very fast. Because Django uses an Object-Relational Mapper (ORM), the exact same application code runs on MySQL or PostgreSQL in production just by setting the environment variables in `.env` without rewriting any SQL."*

### Q10: "If you had 1 more week, what would you add next?"
> *"1. **Resume PDF Parsing:** Allow students to upload PDF resumes and use a library like `pdfplumber` to auto-extract skills.
> 2. **Email Notifications:** Automated alerts via Django email signals when an application status updates to 'Shortlisted' or 'Selected'.
> 3. **Visual Analytics:** Add Chart.js to the staff dashboard to visualize hiring funnels and placement percentages per branch."*

---

## ⚡ 5. Live Demo Cheat Sheet

If the interviewer asks you to run or demonstrate the project:

```bash
# 1. Run the server
python manage.py runserver

# 2. Run automated tests
python manage.py test tracker

# 3. Superuser login
URL: http://127.0.0.1:8000/admin/
Username: admin
Password: admin123

# 4. Key URLs to show:
- Dashboard: http://127.0.0.1:8000/
- Job Search: http://127.0.0.1:8000/jobs/
- Job API: http://127.0.0.1:8000/api/jobs/
- Staff Manager: http://127.0.0.1:8000/manage-applications/
```

**Good luck with the interview! You have a solid, well-architected project to show.**

