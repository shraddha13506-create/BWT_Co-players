import re
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# -------------------------
# 1. Sample Dataset (Replace with real dataset later)
# -------------------------

data = {
    "url_length": [20, 75, 45, 120, 30, 95],
    "num_dots": [1, 4, 2, 6, 1, 5],
    "has_ip": [0, 1, 0, 1, 0, 1],
    "has_at": [0, 1, 0, 1, 0, 0],
    "label": [0, 1, 0, 1, 0, 1]  # 0 = Legit, 1 = Phishing
}

df = pd.DataFrame(data)

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# -------------------------
# 2. Feature Extraction Function
# -------------------------

def extract_features(url):
    url_length = len(url)
    num_dots = url.count(".")
    has_ip = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0
    has_at = 1 if "@" in url else 0

    return np.array([[url_length, num_dots, has_ip, has_at]])

# -------------------------
# 3. Real-Time URL Analysis
# -------------------------

url = input("Enter URL to analyze: ")

features = extract_features(url)

prediction = model.predict(features)[0]
probability = model.predict_proba(features)[0][1] * 100

print("\n--- Analysis Result ---")

if prediction == 1:
    print("⚠️  Potential Phishing URL")
else:
    print("✅ Likely Legitimate URL")

print(f"Risk Score: {probability:.2f}%")

# -------------------------
# 4. Explainable Output
# -------------------------

feature_names = ["URL Length", "Number of Dots", "Has IP", "Has @ Symbol"]
importances = model.feature_importances_

print("\nTop Contributing Features:")
for name, importance in zip(feature_names, importances):
    print(f"{name}: {importance:.3f}")
