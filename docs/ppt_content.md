# PPT Content — Smart Attendance Risk Prediction & Notification System

Use this as a slide-by-slide script. Each "Slide" below = one slide.

---
**Slide 1 — Title**
Smart Attendance Risk Prediction & Notification System
Your Name | Department | College | Date

---
**Slide 2 — Problem Statement**
- Manual attendance tracking gives students no early visibility
- No automated risk classification exists
- Students discover critical attendance too late to fix it

---
**Slide 3 — Objectives**
- Instant student self-service attendance dashboard
- ML-based risk classification (SAFE / MEDIUM / DANGER)
- Auto-calculate classes needed to reach 75%
- Admin panel for bulk data upload and reporting
- Automated email alerts for at-risk students

---
**Slide 4 — Tech Stack**
- Frontend: HTML5, CSS3, JS, Bootstrap 5, Chart.js
- Backend: Python Flask
- Database: SQLite
- ML: scikit-learn, Pandas, NumPy
- Excel: Pandas, OpenPyXL
- Deployment: Render / Railway

---
**Slide 5 — System Architecture (diagram slide)**
Browser (Bootstrap + Chart.js)
   ↓
Flask App (routes, business logic)
   ↓
SQLite DB  ⇄  ML Model (Pickle)  ⇄  Excel Files
   ↓
Flask-Mail (SMTP alerts)

---
**Slide 6 — Student Portal Demo**
- Screenshot of search page
- Screenshot of dashboard with risk badge and charts

---
**Slide 7 — Machine Learning Module**
- Input: Attendance Percentage
- Output: Risk Category
- Model: Decision Tree Classifier
- Training: synthetic 2000-sample dataset, 80/20 split
- Accuracy: ~100% (deterministic rule-based bands)

---
**Slide 8 — Admin Panel Demo**
- Screenshot of Excel upload
- Screenshot of student table + risk distribution chart

---
**Slide 9 — Notification System**
- Trigger: attendance < 65%
- Flask-Mail sends automated warning email
- Example message shown on slide

---
**Slide 10 — Results**
- Successfully classifies risk levels in real time
- Correctly computes classes-needed calculation
- End-to-end tested: search, dashboard, admin upload, report download

---
**Slide 11 — Future Scope**
- SMS/WhatsApp alerts
- Parent/guardian portal
- Time-series attendance trend prediction
- Face-recognition based attendance capture

---
**Slide 12 — Conclusion**
Combines full-stack web development with applied ML to solve a real
academic problem — proactive, data-driven attendance monitoring.

---
**Slide 13 — Thank You / Q&A**
