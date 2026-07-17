"""
train_model.py
---------------
Builds a synthetic training dataset of attendance percentages mapped to
risk categories, trains a Decision Tree Classifier, evaluates it, and
saves it to models/attendance_model.pkl using pickle.

Rules encoded (and learned by the model):
    >= 75%        -> SAFE
    65% - 74.99%  -> MEDIUM RISK
    < 65%         -> DANGER

Run this once (or whenever you want to retrain):
    python train_model.py
"""

import numpy as np
import pandas as pd
import pickle
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# ---------------------------------------------------------
# 1. Create a synthetic dataset (2000 samples, 0-100%)
# ---------------------------------------------------------
np.random.seed(42)
percentages = np.random.uniform(0, 100, 2000)


def label_from_pct(p):
    if p >= 75:
        return "SAFE"
    elif p >= 65:
        return "MEDIUM RISK"
    else:
        return "DANGER"


labels = [label_from_pct(p) for p in percentages]

df = pd.DataFrame({"Attendance_Percentage": percentages, "Risk_Level": labels})

# ---------------------------------------------------------
# 2. Preprocessing
# ---------------------------------------------------------
X = df[["Attendance_Percentage"]]
y = df["Risk_Level"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------------------------------------------
# 3. Train Decision Tree Classifier
# ---------------------------------------------------------
model = DecisionTreeClassifier(max_depth=4, random_state=42)
model.fit(X_train, y_train)

# ---------------------------------------------------------
# 4. Evaluate
# ---------------------------------------------------------
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {acc * 100:.2f}%")
print(classification_report(y_test, y_pred))

# ---------------------------------------------------------
# 5. Save model with pickle
# ---------------------------------------------------------
with open("models/attendance_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved to models/attendance_model.pkl")
