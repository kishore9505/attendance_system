# Viva Questions & Answers

**Q1. What problem does this project solve?**
It gives students real-time visibility into their attendance risk and
automatically alerts students whose attendance drops below the
detention threshold, instead of relying on manual, after-the-fact
tracking.

**Q2. Why did you choose a Decision Tree Classifier over other algorithms?**
Decision Trees are simple, fast, interpretable, and well-suited to a
problem defined by clear threshold rules. Since the risk bands are
essentially piecewise rules over a single numeric feature, a shallow
tree learns the exact boundaries with very high accuracy while
remaining easy to explain to a non-technical evaluator.

**Q3. What is the input and output of your ML model?**
Input: attendance percentage (a single numeric feature).
Output: one of three classes — SAFE, MEDIUM RISK, DANGER.

**Q4. How did you generate your training data?**
Since there was no labeled real-world dataset, I generated a synthetic
dataset of 2000 attendance percentages (uniformly distributed 0–100%)
and labeled each according to the fixed risk rules. This lets the
model learn the exact same logic in a data-driven way.

**Q5. How do you calculate the number of classes needed to reach 75%?**
I solve the inequality `(present + x) / (total + x) >= 0.75` for x,
which gives the minimum number of additional classes (assuming all are
attended) needed to reach the 75% target.

**Q6. Why did you use SQLite instead of MySQL/PostgreSQL?**
SQLite is serverless, file-based, and requires no separate database
server setup — ideal for a college project or small-scale deployment.
The same logic could be migrated to PostgreSQL/MySQL for production
scale without major code changes, since Flask abstracts the queries.

**Q7. How does the Excel upload feature work?**
The admin uploads an `.xlsx` file through a form. Flask receives it via
`request.files`, saves it to the `uploads/` folder, and Pandas reads it
into a DataFrame. Each row is inserted or updated into the SQLite
`students` table using an `INSERT ... ON CONFLICT` upsert query keyed
on roll number.

**Q8. How are email notifications triggered?**
Whenever a student's dashboard is loaded and the computed risk level is
DANGER, the app calls a Flask-Mail function that sends a warning email
to the student's registered email address via SMTP.

**Q9. What is Flask-Mail and how did you configure it?**
Flask-Mail is a Flask extension for sending email via SMTP. It's
configured with the mail server (`smtp.gmail.com`), port, TLS setting,
and Gmail credentials (using an App Password, not the account
password) supplied as environment variables.

**Q10. How would you deploy this project?**
Push the code to GitHub, then connect the repository to Render or
Railway. Set the build command to install `requirements.txt` and the
start command to run the app with Gunicorn (`gunicorn app:app`).
Environment variables for email credentials are configured in the
platform's dashboard.

**Q11. What is glassmorphism and why did you use it in the UI?**
Glassmorphism is a design style using translucent, blurred "frosted
glass" panels over colorful backgrounds. It was used here to make the
dashboard look modern and visually layered while keeping the interface
clean and readable.

**Q12. How is Chart.js used in this project?**
Chart.js renders the attendance doughnut chart on the student
dashboard and the risk-distribution pie chart plus department-wise bar
chart on the admin panel, using data passed from Flask via Jinja
templating into JavaScript.

**Q13. How would you scale this system for a whole college?**
Move from SQLite to PostgreSQL, add pagination and indexing to the
admin student table, cache the ML model in memory (already done here),
and consider migrating heavy Excel processing to a background task
queue (e.g., Celery) for very large uploads.

**Q14. What security measures are present, and what would you add for production?**
Currently: session-based admin login and file-type validation on
uploads. For production: hash admin passwords (e.g., with bcrypt),
use HTTPS, add CSRF protection on forms, validate/sanitize Excel
content more strictly, and move the secret key and mail credentials
fully into environment variables/secrets management.

**Q15. What was the most challenging part of this project?**
Designing the "classes needed to reach 75%" formula correctly and
making sure the ML risk classification, the Excel upload pipeline, and
the email notification trigger all stayed consistent with each other
so the risk badge shown to a student always matches the backend logic.
