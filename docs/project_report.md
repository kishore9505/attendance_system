# Project Report: Smart Attendance Risk Prediction & Notification System

## 1. Abstract
Poor attendance is a leading cause of academic detention in colleges, yet
students often only discover the severity of their situation right before
exams. This project presents a web-based Smart Attendance Risk Prediction
& Notification System that lets students instantly check their attendance
health, understand their risk category through a machine learning model,
and see exactly how many additional classes they must attend to recover.
Administrators can bulk-upload attendance data from Excel, monitor
department-wide statistics, and the system automatically emails
students who fall into the critical "DANGER" zone.

## 2. Problem Statement
Manual attendance tracking in colleges is fragmented across spreadsheets
and physical registers, giving students little visibility into their own
standing until it is too late. There is no automated early-warning
mechanism, no data-driven risk classification, and no proactive
communication channel to alert at-risk students in time for corrective
action.

## 3. Objectives
- Provide students instant, self-service access to their attendance analytics.
- Classify each student's risk level (SAFE / MEDIUM RISK / DANGER) using
  a trained machine learning model rather than hardcoded thresholds alone.
- Calculate the exact number of additional classes needed to reach the
  75% attendance requirement.
- Give administrators a centralized dashboard to upload data, monitor
  statistics, and export reports.
- Automatically notify at-risk students via email.

## 4. System Architecture
The system follows a classic three-tier web architecture:

- **Presentation Layer**: HTML5/CSS3/Bootstrap 5 templates rendered by
  Flask (Jinja2), with Chart.js for data visualization and vanilla
  JavaScript for interactivity.
- **Application Layer**: A Python Flask backend exposing routes for
  student search, dashboard rendering, JSON APIs, and admin operations
  (login, upload, reporting).
- **Data Layer**: SQLite stores structured student attendance records;
  Excel files (read/written via Pandas and OpenPyXL) serve as the
  external data exchange format for uploads and report downloads.
- **Intelligence Layer**: A scikit-learn Decision Tree Classifier,
  trained offline and serialized with Pickle, is loaded by the Flask
  app at runtime to classify risk level from attendance percentage.
- **Notification Layer**: Flask-Mail sends SMTP email alerts to
  students whose attendance drops below 65%.

## 5. Methodology
1. **Data Ingestion**: Admin uploads an Excel file with student
   attendance data. Pandas parses it and OpenPyXL/SQLite persist it.
2. **Preprocessing**: Attendance percentage is derived from
   `present_classes / total_classes * 100` for every student.
3. **Model Training**: A synthetic labeled dataset (2000 samples)
   spanning 0–100% attendance was generated, with labels assigned
   according to the fixed risk-band rules. An 80/20 train-test split
   was used, and a Decision Tree Classifier (max depth 4) was trained
   and evaluated using accuracy and a classification report.
4. **Model Deployment**: The trained model is serialized with
   `pickle` and loaded once at Flask app startup for fast, repeated
   inference.
5. **Improvement Calculator**: A closed-form formula computes the
   minimum number of consecutive future classes a student must attend
   to reach the 75% target, solving:
   `(present + x) / (total + x) >= 0.75`
6. **Notification**: When a student's computed risk level is DANGER,
   the system automatically composes and sends a warning email.

## 6. Technologies Used
- **Languages**: Python, HTML, CSS, JavaScript
- **Backend Framework**: Flask
- **Frontend Framework**: Bootstrap 5, Chart.js
- **Database**: SQLite
- **ML Libraries**: scikit-learn, Pandas, NumPy
- **Excel Handling**: Pandas, OpenPyXL
- **Email**: Flask-Mail (SMTP)
- **Deployment**: Render / Railway, Gunicorn

## 7. Results
The Decision Tree Classifier achieved near-perfect accuracy on the
synthetic test set, since the risk bands are deterministic thresholds
that a shallow tree can learn exactly. The web application was manually
tested end-to-end: student search, dashboard rendering with correct
risk color-coding, admin Excel upload and re-processing, chart
rendering, and Excel report export all function correctly.

## 8. Future Scope
- Incorporate SMS/WhatsApp alerts alongside email.
- Add parent/guardian accounts with independent notifications.
- Move from static thresholds to a time-series model that predicts
  attendance trajectory over a semester.
- Integrate biometric or face-recognition based attendance capture to
  remove manual Excel uploads entirely.
- Add role-based access control (faculty, HOD, admin) with granular
  permissions.

## 9. Conclusion
This project demonstrates how a relatively simple machine learning
model, combined with a well-designed full-stack web application, can
meaningfully improve transparency and proactive intervention in
academic attendance management. It brings together frontend design,
backend engineering, data processing, and applied machine learning
into a single, deployable, real-world system suitable for both
academic submission and further extension as an internship project.
