import re
import numpy as np
import joblib
import pytesseract
from PIL import Image
from src.url_features import extract_features
from src.hybrid import sender_spam_check

# Load Models
url_model = joblib.load("models/url_model.pkl")
sms_model = joblib.load("models/sms_model.pkl")
vectorizer = joblib.load("models/sms_vectorizer.pkl")

# -------------------------
# URL Prediction
# -------------------------

url = input("Enter URL to analyze: ")

features = extract_features(url)

prediction = url_model.predict(features)[0]
probability = url_model.predict_proba(features)[0][1] * 100

print("\n--- Analysis Result ---")

if prediction == 1:
    print("⚠️  Potential Phishing URL")
else:
    print("✅ Likely Legitimate URL")

print(f"Risk Score: {probability:.2f}%")

# -------------------------
# SMS Prediction
# -------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def predict_sms(text):
    text = clean_text(text)
    text_vec = vectorizer.transform([text])
    prediction = sms_model.predict(text_vec)[0]
    probability = sms_model.predict_proba(text_vec)[0][1]
    
    if prediction == 1:
        return f"🚨 SPAM (Confidence: {probability*100:.2f}%)"
    else:
        return f"✅ NOT SPAM (Confidence: {(1-probability)*100:.2f}%)"

print("\nChoose Input Method:")
print("1 → Type SMS manually")
print("2 → Upload Screenshot Image")
print("3 → Exit")

choice = input("Enter choice (1/2/3): ")

if choice == "1":
    user_text = input("\nEnter your SMS: ")
    result = predict_sms(user_text)
    print("Prediction:", result)

elif choice == "2":
    image_path = input("Enter image path: ")
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img)
    
    print("\nExtracted Text:")
    print(extracted_text)
    
    result = predict_sms(extracted_text)
    print("\nPrediction from Image:", result)

elif choice == "3":
    print("Program Ended.")
