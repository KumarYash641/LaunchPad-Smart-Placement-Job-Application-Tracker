import os, django
os.environ["DJANGO_SETTINGS_MODULE"] = "placement_project.settings"
django.setup()

from tracker.models import Company, Job
from datetime import date, timedelta

today = date.today()

companies_data = [
    {"name": "Google", "website": "https://careers.google.com", "location": "Bangalore", "description": "Leading technology company specializing in search, cloud computing, and AI."},
    {"name": "Microsoft", "website": "https://careers.microsoft.com", "location": "Hyderabad", "description": "Global leader in software, cloud services, and enterprise solutions."},
    {"name": "Amazon", "website": "https://www.amazon.jobs", "location": "Bangalore", "description": "E-commerce and cloud computing giant powering AWS and retail innovation."},
    {"name": "Infosys", "website": "https://www.infosys.com/careers", "location": "Pune", "description": "Leading Indian IT services and consulting company."},
    {"name": "TCS", "website": "https://www.tcs.com/careers", "location": "Mumbai", "description": "Tata Consultancy Services - India's largest IT services company."},
    {"name": "Flipkart", "website": "https://www.flipkartcareers.com", "location": "Bangalore", "description": "India's leading e-commerce marketplace."},
    {"name": "Razorpay", "website": "https://razorpay.com/careers", "location": "Bangalore", "description": "Full-stack fintech company offering payment gateway and banking solutions."},
    {"name": "Zoho", "website": "https://www.zoho.com/careers", "location": "Chennai", "description": "SaaS company offering business, collaboration, and productivity software."},
]

companies = {}
for data in companies_data:
    comp, created = Company.objects.get_or_create(name=data["name"], defaults=data)
    companies[data["name"]] = comp
    status = "Created" if created else "Exists"
    print(f"  {status}: {comp.name}")

jobs_data = [
    {"title": "Software Engineer", "company": "Google", "description": "Design and build scalable backend systems using Python and Go. Work on large-scale distributed systems that serve billions of users. Collaborate with cross-functional teams on product features.", "location": "Bangalore", "employment_type": "Full-time", "min_cgpa": 8.0, "required_skills": "Python, Data Structures, Algorithms, SQL", "deadline": today + timedelta(days=30)},
    {"title": "Data Analyst Intern", "company": "Google", "description": "Analyze large datasets to drive business decisions. Build dashboards and reports using SQL and Python. Work with product teams to define and track key metrics.", "location": "Hyderabad", "employment_type": "Internship", "min_cgpa": 7.5, "required_skills": "Python, SQL, Excel, Statistics", "deadline": today + timedelta(days=20)},
    {"title": "Full Stack Developer", "company": "Microsoft", "description": "Develop cloud-based web applications using React and .NET. Participate in code reviews and agile sprints. Build microservices deployed on Azure cloud platform.", "location": "Hyderabad", "employment_type": "Full-time", "min_cgpa": 7.5, "required_skills": "JavaScript, React, Python, SQL", "deadline": today + timedelta(days=25)},
    {"title": "Cloud Support Engineer", "company": "Amazon", "description": "Provide technical support for AWS services. Troubleshoot customer issues related to EC2, S3, Lambda, and networking. Write internal knowledge base articles.", "location": "Bangalore", "employment_type": "Full-time", "min_cgpa": 7.0, "required_skills": "Linux, Networking, Python, AWS", "deadline": today + timedelta(days=15)},
    {"title": "SDE Intern", "company": "Amazon", "description": "Work on real-world projects within Amazon's engineering team. Build features for customer-facing applications. Gain hands-on experience with large-scale systems.", "location": "Hyderabad", "employment_type": "Internship", "min_cgpa": 7.0, "required_skills": "Java, Data Structures, Algorithms", "deadline": today + timedelta(days=18)},
    {"title": "Systems Engineer", "company": "Infosys", "description": "Join the flagship training program and work on enterprise Java projects. Develop and maintain client applications. Participate in the full software development lifecycle.", "location": "Pune", "employment_type": "Full-time", "min_cgpa": 6.0, "required_skills": "Java, SQL, HTML, CSS", "deadline": today + timedelta(days=35)},
    {"title": "Python Developer", "company": "Infosys", "description": "Build automation scripts and backend APIs using Python and Django. Work with databases and REST services. Collaborate with global delivery teams.", "location": "Mysore", "employment_type": "Full-time", "min_cgpa": 6.5, "required_skills": "Python, Django, SQL", "deadline": today + timedelta(days=28)},
    {"title": "Assistant System Engineer", "company": "TCS", "description": "Entry-level role for fresh graduates. Training provided in Java, cloud, and enterprise technologies. Work on client projects across banking, retail, and healthcare.", "location": "Mumbai", "employment_type": "Full-time", "min_cgpa": 6.0, "required_skills": "Java, SQL, HTML", "deadline": today + timedelta(days=40)},
    {"title": "Frontend Developer", "company": "Flipkart", "description": "Build responsive and performant UI for Flipkart web and mobile platforms. Optimize for speed and user experience. Work closely with designers and product managers.", "location": "Bangalore", "employment_type": "Full-time", "min_cgpa": 7.0, "required_skills": "JavaScript, React, HTML, CSS", "deadline": today + timedelta(days=22)},
    {"title": "Backend Engineer Intern", "company": "Razorpay", "description": "Build payment processing APIs and microservices. Work with Go and Python on fintech infrastructure. Learn about payment systems and financial regulations.", "location": "Bangalore", "employment_type": "Internship", "min_cgpa": 7.5, "required_skills": "Python, SQL, REST APIs", "deadline": today + timedelta(days=14)},
    {"title": "Software Developer", "company": "Zoho", "description": "Develop modules for Zoho SaaS products. Work on full-stack features using Java and JavaScript. Permanent WFO role with excellent learning culture.", "location": "Chennai", "employment_type": "Full-time", "min_cgpa": 6.5, "required_skills": "Java, JavaScript, SQL, HTML", "deadline": today + timedelta(days=30)},
    {"title": "QA Engineer", "company": "Zoho", "description": "Write automated test suites using Selenium and Python. Perform regression, integration, and performance testing. Ensure software quality across product releases.", "location": "Chennai", "employment_type": "Contract", "min_cgpa": 6.0, "required_skills": "Python, Selenium, SQL", "deadline": today + timedelta(days=25)},
]

count = 0
for data in jobs_data:
    comp = companies[data.pop("company")]
    job, created = Job.objects.get_or_create(title=data["title"], company=comp, defaults=data)
    if created:
        count += 1
    status = "Created" if created else "Exists"
    print(f"  {status}: {job}")

print(f"\nDone! Added {count} jobs across {len(companies)} companies.")

