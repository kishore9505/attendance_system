"""
app.py
------
Smart Attendance Risk Prediction & Notification System
Main Flask application.

Run with:
    python app.py

Then open http://127.0.0.1:5000
"""

import os
import io
import pickle
import sqlite3
from functools import wraps

import pandas as pd
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, send_file, jsonify
)
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

# ------------------------------------------------------------------
# App configuration
# ------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "change-this-secret-key-in-production"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "students.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
MODEL_PATH = os.path.join(BASE_DIR, "models", "attendance_model.pkl")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = {"xlsx", "xls"}

# ------------------------------------------------------------------
# Flask-Mail configuration
# Gmail requires an "App Password", not your normal password.
# Set these before running the app:
#   $env:MAIL_USERNAME="your_email@gmail.com"
#   $env:MAIL_PASSWORD="your_16_char_app_password"
# ------------------------------------------------------------------
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = app.config["MAIL_USERNAME"]

mail = Mail(app)

if not app.config["MAIL_USERNAME"] or not app.config["MAIL_PASSWORD"]:
    print("[MAIL] Set MAIL_USERNAME and MAIL_PASSWORD environment variables to enable email sending.")

# Admin credentials (for a real project, store these hashed in the DB)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ------------------------------------------------------------------
# Database helpers
# ------------------------------------------------------------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            branch TEXT,
            total_classes INTEGER,
            present_classes INTEGER,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()


def _clean_excel_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def _clean_excel_int(value, default=0):
    if pd.isna(value):
        return default
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def load_excel_to_db(filepath):
    """Reads an Excel file and replaces the SQLite student records with its contents."""
    df = pd.read_excel(filepath)
    required_cols = {"Roll_No", "Name", "Branch", "Total_Classes", "Present_Classes", "Email"}
    if not required_cols.issubset(set(df.columns)):
        raise ValueError(f"Excel must contain columns: {required_cols}")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students")

    for _, row in df.iterrows():
        roll_no = _clean_excel_text(row["Roll_No"])
        if not roll_no:
            continue

        cur.execute("""
            INSERT INTO students (roll_no, name, branch, total_classes, present_classes, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            roll_no,
            _clean_excel_text(row["Name"]),
            _clean_excel_text(row["Branch"]),
            _clean_excel_int(row["Total_Classes"]),
            _clean_excel_int(row["Present_Classes"]),
            _clean_excel_text(row["Email"])
        ))

    conn.commit()
    count = cur.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    conn.close()
    return count


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


# ------------------------------------------------------------------
# ML model loading
# ------------------------------------------------------------------
_model = None


def get_model():
    global _model
    if _model is None:
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    return _model


def predict_risk(percentage):
    """Uses the trained Decision Tree model to classify risk level."""
    model = get_model()
    input_df = pd.DataFrame([[percentage]], columns=["Attendance_Percentage"])
    prediction = model.predict(input_df)[0]
    return prediction



# ------------------------------------------------------------------
# Business logic
# ------------------------------------------------------------------
def compute_attendance(total, present):
    if total == 0:
        return 0.0
    return round((present / total) * 100, 2)


def risk_color(risk_level):
    return {
        "SAFE": "green",
        "MEDIUM RISK": "yellow",
        "DANGER": "red",
    }.get(risk_level, "gray")


def classes_needed_for_target(total, present, target_pct=75.0):
    """
    Calculates how many MORE classes (all attended) a student must
    attend so that present/(total+x) >= target_pct/100.

    present + x >= target_pct/100 * (total + x)
    Solve for x.
    """
    if total == 0:
        return 0
    current_pct = (present / total) * 100
    if current_pct >= target_pct:
        return 0

    target = target_pct / 100
    # x >= (target*total - present) / (1 - target)
    numerator = (target * total) - present
    denominator = 1 - target
    x = numerator / denominator
    return max(0, int(x) + 1)  # round up


def send_risk_alert_email(name, email, roll_no, percentage):
    """Sends a warning email if attendance is below 65%."""
    try:
        if not app.config.get("MAIL_USERNAME") or not app.config.get("MAIL_PASSWORD"):
            print("[Email not sent] MAIL_USERNAME or MAIL_PASSWORD is not configured.")
            return False

        msg = Message(
            subject="⚠️ Attendance Warning - Immediate Action Required",
            recipients=[email],
            body=(
                f"Dear {name} ({roll_no}),\n\n"
                f"Warning! Your attendance has fallen below 65% "
                f"(current: {percentage}%).\n"
                f"Please attend classes regularly to avoid detention.\n\n"
                f"- Smart Attendance Risk Prediction System"
            )
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"[Email not sent] {type(e).__name__}: {e}")
        return False


# ------------------------------------------------------------------
# Auth decorator for admin routes
# ------------------------------------------------------------------
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


# ------------------------------------------------------------------
# Routes - Student portal
# ------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    roll_no = request.form.get("roll_no", "").strip()
    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE roll_no = ?", (roll_no,)
    ).fetchone()
    conn.close()

    if student is None:
        flash("No student found with that roll number.", "danger")
        return redirect(url_for("index"))

    return redirect(url_for("dashboard", roll_no=roll_no))


@app.route("/dashboard/<roll_no>")
def dashboard(roll_no):
    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE roll_no = ?", (roll_no,)
    ).fetchone()
    conn.close()

    if student is None:
        flash("Student not found.", "danger")
        return redirect(url_for("index"))

    percentage = compute_attendance(student["total_classes"], student["present_classes"])
    risk_level = predict_risk(percentage)
    color = risk_color(risk_level)
    needed = classes_needed_for_target(student["total_classes"], student["present_classes"])

    # Trigger email alert if in DANGER zone
    email_sent = False
    if risk_level == "DANGER":
        email_sent = send_risk_alert_email(student["name"], student["email"], roll_no, percentage)

    return render_template(
        "dashboard.html",
        student=student,
        percentage=percentage,
        risk_level=risk_level,
        color=color,
        needed=needed,
        email_sent=email_sent
    )


@app.route("/api/student/<roll_no>")
def api_student(roll_no):
    """JSON endpoint used by script.js to render Chart.js graphs."""
    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE roll_no = ?", (roll_no,)
    ).fetchone()
    conn.close()
    if student is None:
        return jsonify({"error": "not found"}), 404

    percentage = compute_attendance(student["total_classes"], student["present_classes"])
    return jsonify({
        "roll_no": student["roll_no"],
        "name": student["name"],
        "branch": student["branch"],
        "total_classes": student["total_classes"],
        "present_classes": student["present_classes"],
        "percentage": percentage,
        "risk_level": predict_risk(percentage)
    })


# ------------------------------------------------------------------
# Routes - Admin panel
# ------------------------------------------------------------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin_panel"))
        flash("Invalid admin credentials.", "danger")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("index"))


@app.route("/admin")
@admin_required
def admin_panel():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    enriched = []
    risk_counts = {"SAFE": 0, "MEDIUM RISK": 0, "DANGER": 0}
    branch_totals = {}

    for s in students:
        pct = compute_attendance(s["total_classes"], s["present_classes"])
        risk = predict_risk(pct)
        risk_counts[risk] = risk_counts.get(risk, 0) + 1

        branch_totals.setdefault(s["branch"], []).append(pct)

        enriched.append({
            "roll_no": s["roll_no"],
            "name": s["name"],
            "branch": s["branch"],
            "total_classes": s["total_classes"],
            "present_classes": s["present_classes"],
            "percentage": pct,
            "risk_level": risk
        })

    branch_avg = {
        branch: round(sum(vals) / len(vals), 2)
        for branch, vals in branch_totals.items()
    }

    return render_template(
        "admin.html",
        students=enriched,
        risk_counts=risk_counts,
        branch_avg=branch_avg
    )


@app.route("/admin/upload", methods=["POST"])
@admin_required
def admin_upload():
    if "excel_file" not in request.files:
        flash("No file part in request.", "danger")
        return redirect(url_for("admin_panel"))

    file = request.files["excel_file"]
    if file.filename == "":
        flash("No file selected.", "danger")
        return redirect(url_for("admin_panel"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        try:
            count = load_excel_to_db(filepath)
            flash(f"Excel uploaded successfully. {count} students in database.", "success")
        except Exception as e:
            flash(f"Error processing Excel file: {e}", "danger")
    else:
        flash("Only .xlsx or .xls files are allowed.", "danger")

    return redirect(url_for("admin_panel"))


@app.route("/admin/download_report")
@admin_required
def download_report():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    rows = []
    for s in students:
        pct = compute_attendance(s["total_classes"], s["present_classes"])
        rows.append({
            "Roll_No": s["roll_no"],
            "Name": s["name"],
            "Branch": s["branch"],
            "Total_Classes": s["total_classes"],
            "Present_Classes": s["present_classes"],
            "Attendance_Percentage": pct,
            "Risk_Level": predict_risk(pct)
        })

    df = pd.DataFrame(rows)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Attendance Report")
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="attendance_report.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.route("/admin/send_notification/<roll_no>", methods=["POST"])
@admin_required
def send_notification(roll_no):
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,)).fetchone()
    conn.close()

    if student is None:
        flash("Student not found.", "danger")
        return redirect(url_for("admin_panel"))

    message = (
        f"Hello {student['name']},\n\n"
        f"This is a reminder from the attendance admin. Please attend classes regularly to improve your attendance.\n"
        f"Your current attendance is {compute_attendance(student['total_classes'], student['present_classes'])}%."
    )

    sent = False
    try:
        if not app.config.get("MAIL_USERNAME") or not app.config.get("MAIL_PASSWORD"):
            print("[Notification failed] MAIL_USERNAME or MAIL_PASSWORD is not configured.")
        else:
            msg = Message(
                subject="Attendance Reminder from Admin",
                recipients=[student["email"]],
                body=message,
            )
            mail.send(msg)
            sent = True
    except Exception as e:
        print(f"[Notification failed] {type(e).__name__}: {e}")

    if sent:
        flash(f"Notification sent to {student['name']} ({student['email']}).", "success")
    else:
        flash("Notification failed. Please verify the email configuration.", "danger")

    return redirect(url_for("admin_panel"))


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------
if __name__ == "__main__":
    init_db()
    excel_path = os.path.join(BASE_DIR, "attendance.xlsx")
    if os.path.exists(excel_path):
        count = load_excel_to_db(excel_path)
        print(f"Loaded {count} students from attendance.xlsx into database.")

    app.run(debug=True)
