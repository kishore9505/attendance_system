"""
generate_sample_excel.py
-------------------------
Creates a sample attendance.xlsx file with the required columns:
Roll_No, Name, Branch, Total_Classes, Present_Classes, Email

Run this once to create test data:
    python generate_sample_excel.py
"""

import pandas as pd
import random

branches = ["CSD", "CSE", "ECE", "MECH", "CIVIL"]
first_names = ["Aarav", "Vihaan", "Kishore", "Rohan", "Sai", "Aditya", "Karthik",
               "Priya", "Ananya", "Sneha", "Divya", "Meena", "Ravi", "Suresh", "Anitha"]
last_names = ["Reddy", "Sharma", "Naidu", "Kumar", "Rao", "Verma", "Nair", "Iyer"]

random.seed(42)
rows = []
for i in range(1, 61):  # 60 sample students
    roll_no = f"22CSD{i:03d}"
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    branch = random.choice(branches)
    total_classes = random.randint(80, 100)
    # Deliberately spread attendance across SAFE / MEDIUM / DANGER bands
    band = random.choice(["safe", "medium", "danger"])
    if band == "safe":
        pct = random.uniform(0.75, 0.98)
    elif band == "medium":
        pct = random.uniform(0.65, 0.7499)
    else:
        pct = random.uniform(0.35, 0.6499)
    present_classes = int(total_classes * pct)
    email = f"{name.split()[0].lower()}{i}@example.com"
    rows.append([roll_no, name, branch, total_classes, present_classes, email])

df = pd.DataFrame(rows, columns=["Roll_No", "Name", "Branch", "Total_Classes", "Present_Classes", "Email"])
df.to_excel("attendance.xlsx", index=False)
print("attendance.xlsx created with", len(df), "sample students.")
