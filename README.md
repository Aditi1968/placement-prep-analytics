# Placement Prep Analytics & Repository System (PPARS)

👩‍💻 **Author:** *Aditi Vadmal*  
📍 Bangalore | 🎓 Computer Science Student  

---

## 📌 Project Overview
This project was built as part of my **internship work under Scaler’s Learning Outcome & Career Outcome (Lo/Co) team**.  
It is a full-stack analytics system designed to improve **interview preparation, learner enablement, and career outcomes**.  

The system helps track learner performance, generate last-minute tests, analyze failure reasons, and coordinate bootcamps — exactly the type of interventions Scaler uses to improve placement results.

---

## 🎯 Features
- **Interview Repository**  
  Centralized question bank categorized by company, role, and difficulty.  

- **Test Generator**  
  Automatically create last-minute interview prep tests.  

- **Gap Analysis**  
  Record learner attempts and failure reasons → highlight top weaknesses.  

- **Impact Analytics**  
  KPI dashboard with charts like “Success Rate by Company” and “Top Failure Reasons.”  

- **Survey Insights**  
  Import CSV learner feedback → sentiment + theme tagging.  

- **Bootcamp Scheduler**  
  Plan weekend bootcamps and export `.ics` calendar invites for learners.

---

## 🛠 Tech Stack
- **Backend:** Python, Flask, SQLAlchemy  
- **Database:** SQLite (easy to migrate to PostgreSQL/MySQL)  
- **Data Analysis:** Pandas, Matplotlib  
- **Frontend:** Jinja2 templates + CSS (dark theme)  
- **Deployment:** Render / Railway / Heroku (Gunicorn)

---

## 🚀 Quickstart

```bash
# Clone repo
git clone https://github.com/Aditi1968/placement-prep-analytics.git
cd placement-prep-analytics/backend

# Setup environment
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with sample data
python seed.py

# Run locally
gunicorn backend.app:app
# open http://127.0.0.1:8000
