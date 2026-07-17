# 🎓 Smart Attendance Risk Prediction & Notification System

A full-stack college attendance monitoring web app. Students enter their
roll number to instantly see their attendance analytics, ML-predicted risk
level, and exactly how many classes they must attend to reach 75%.
Admins upload Excel attendance sheets, view stats, and download reports.
At-risk students automatically get an email alert.

## ✨ Features
- Student search portal with instant analytics
- Risk level detection (SAFE / MEDIUM RISK / DANGER) via a trained
  Decision Tree Classifier (scikit-learn)
- Attendance improvement calculator ("attend X more classes to reach 75%")
- Modern glassmorphism dashboard with Chart.js visualizations
- Admin panel: Excel upload, student list, risk stats, downloadable report
- Automatic email notifications (Flask-Mail) for students below 65%
- SQLite database, Pandas/OpenPyXL Excel processing

## 🧰 Tech Stack
| Layer          | Technology                              |
|----------------|------------------------------------------|
| Frontend       | HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js |
| Backend        | Python, Flask                            |
| Database       | SQLite                                   |
| Machine Learning | scikit-learn (Decision Tree), Pandas, NumPy |
| Excel Handling | Pandas, OpenPyXL                         |
| Email          | Flask-Mail                               |
| Deployment     | Render / Railway                         |

## 📁 Project Structure
```
attendance_system/
├── app.py                     # Main Flask application
├── train_model.py             # Trains & saves the ML model
├── generate_sample_excel.py   # Creates sample attendance.xlsx
├── requirements.txt
├── students.db                # SQLite DB (auto-created on first run)
├── attendance.xlsx            # Sample data
├── models/
│   └── attendance_model.pkl
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── admin_login.html
│   └── admin.html
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── images/
├── uploads/                   # Uploaded Excel files land here
└── docs/                      # Project report, PPT content, viva Q&A
```

## 🚀 Setup Instructions (VS Code, beginner-friendly)

1. **Open the folder** in VS Code.
2. **Create a virtual environment** (recommended):
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```
3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```
4. **(Optional) Regenerate sample data / retrain the model**:
   ```
   python generate_sample_excel.py
   python train_model.py
   ```
5. **Run the app**:
   ```
   python app.py
   ```
6. Open **http://127.0.0.1:5000** in your browser.
   - Try roll numbers `22CSD001` to `22CSD060`.
   - Admin login: **username** `admin`, **password** `admin123` at `/admin/login`.

## 📧 Enabling Real Email Alerts
By default, email sending fails silently (so the app still works without
credentials). To enable real emails:
1. Use a Gmail account and create an **App Password** (Google Account →
   Security → 2-Step Verification → App Passwords).
2. Set environment variables before running:
   ```
   set MAIL_USERNAME=youremail@gmail.com      # Windows
   set MAIL_PASSWORD=your_16_char_app_password
   ```
   (use `export` instead of `set` on Mac/Linux)
3. Restart `python app.py`.

## ☁️ Deployment (Render)
1. Push this project to a GitHub repository.
2. On [render.com](https://render.com), create a **New Web Service** →
   connect your repo.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Add environment variables `MAIL_USERNAME` / `MAIL_PASSWORD` in the
   Render dashboard if you want live email alerts.

## 📊 Excel Format Required for Upload
| Roll_No   | Name        | Branch | Total_Classes | Present_Classes | Email             |
|-----------|-------------|--------|----------------|------------------|--------------------|
| 22CSD001  | Aarav Reddy | CSD    | 90             | 70               | aarav1@example.com |

## 🧠 Machine Learning Model
- **Input**: Attendance Percentage
- **Output**: SAFE / MEDIUM RISK / DANGER
- **Algorithm**: Decision Tree Classifier
- Trained on a synthetic 2000-row dataset with the exact rule boundaries
  (≥75, 65–74.99, <65), saved as `models/attendance_model.pkl`.

## 📄 Documentation
See the `docs/` folder for the Project Report, PPT content, and Viva
Questions & Answers — ready for internship or academic submission.

## 🔮 Future Scope
- SMS/WhatsApp notifications in addition to email
- Parent/guardian login and notifications
- Attendance prediction trends over the semester (time-series ML)
- Face-recognition based automatic attendance capture
- Role-based access (faculty vs HOD vs admin)

## 👤 Author
Built as a personal/internship project by **Kishore** — B.Tech Data Science.
