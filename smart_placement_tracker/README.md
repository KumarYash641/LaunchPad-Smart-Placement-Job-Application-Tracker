# LaunchPad — Smart Placement & Job Application Tracker

An intermediate full-stack portfolio project built with **Python, Django, Django REST Framework, MySQL/SQLite, HTML, CSS and JavaScript**.

## Features included

- Student registration, login and profile management
- Student profile with CGPA, skills, education and resume URL
- Company and job management through Django Admin
- Job search by role, company, location and skills
- Eligibility checker based on minimum CGPA, required skills and deadline
- Job applications with duplicate-application protection
- Application status tracking
- Staff page to update application statuses
- Dashboard with application counts and eligible opportunities
- Read-only REST endpoints for jobs and the logged-in student's applications

## Requirements

- Python 3.10+
- pip
- Optional: MySQL Server and MySQL Workbench
- Optional: MySQL driver (`mysqlclient`) if you choose MySQL

## Run locally (SQLite — easiest first run)

SQLite is configured by default, so you can run the project without installing MySQL first.

### Windows

```bash
# 1. Open a terminal in this folder
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create database tables
python manage.py makemigrations tracker
python manage.py migrate

# 4. Create an admin account
python manage.py createsuperuser

# 5. Start the development server
python manage.py runserver
```

Open:
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Jobs API: http://127.0.0.1:8000/api/jobs/
- My applications API (login required): http://127.0.0.1:8000/api/my-applications/

## Add sample data

1. Log in to `/admin/` using the superuser.
2. Add one or more **Companies**.
3. Add **Jobs** and set `min_cgpa`, `required_skills`, and an optional deadline.
4. Register a normal student account from the website.
5. Open the student profile and enter CGPA and comma-separated skills.
6. Browse jobs and test the eligibility checker and application flow.

## Use MySQL instead of SQLite

1. Create a database in MySQL:

```sql
CREATE DATABASE placement_tracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Install the MySQL driver:

```bash
pip install mysqlclient
```

3. Copy `.env.example` to `.env`.
4. Set these values in `.env`:

```env
SECRET_KEY=use-a-long-random-secret
DEBUG=True
DB_ENGINE=mysql
DB_NAME=placement_tracker
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

5. Run migrations again:

```bash
python manage.py migrate
```

If `mysqlclient` installation fails on Windows, continue with SQLite for development first. The application code uses Django's ORM and supports MySQL once the driver and database are configured.

## Main project structure

```text
placement_project/   Django project configuration
tracker/             Models, forms, views, services and API
templates/            HTML templates
static/css/           Styles
static/js/            JavaScript
```

## Important model relationships

- A Django User has one StudentProfile.
- A Company can have many Jobs.
- A Job can have many Applications.
- A User can submit many Applications.
- A database uniqueness constraint prevents the same student applying to the same job twice.

## Before publishing to GitHub or deploying

- Change `SECRET_KEY` and set `DEBUG=False`.
- Configure `ALLOWED_HOSTS`.
- Use environment variables for secrets and database credentials.
- Add production static-file handling and HTTPS.
- Review permissions and test all workflows.
- Never commit `.env`, database files or passwords.

## Suggested next improvements

- Add resume file uploads with file-type and size validation.
- Add pagination to admin application management.
- Add automated tests for eligibility and duplicate applications.
- Add charts using Chart.js.
- Add email notifications for status changes.
- Add richer REST APIs with role-based permissions and automated API tests.

This is a starter implementation for learning and portfolio development. Test it locally, add your own sample data, and understand each module before listing it as a completed project on your resume.
