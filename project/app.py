import streamlit as st
import pickle
import sys
import os
import re
import numpy as np
import pytesseract
from PIL import Image

# Allow access to parent folder (so src works)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.url_features import extract_features

# Load models
url_phishing_model = pickle.load(open("../models/url_model.pkl", "rb"))
sms_spam_model = pickle.load(open("../models/sms_model.pkl", "rb"))
vectorizer = pickle.load(open("../models/sms_vectorizer.pkl", "rb"))

# -----------------------------
# Page Title
# -----------------------------
st.set_page_config(page_title="Email & SMS Safety Assistant", layout="centered")
st.title("🔐 Real-Time Email & SMS Safety Assistant")

st.markdown("---")

# -----------------------------
# URL PHISHING SECTION
# -----------------------------
st.header("🌐 URL Phishing Detection")

url = st.text_input("Enter URL to analyze:")

if st.button("Analyze URL"):
    if url.strip() == "":
        st.warning("Please enter a URL.")
    else:
        features = extract_features(url)
        prediction = url_phishing_model.predict(features)[0]
        probability = url_phishing_model.predict_proba(features)[0][1] * 100

        if prediction == 1:
            st.error(f"⚠️ Potential Phishing URL\n\nRisk Score: {probability:.2f}%")
        else:
            st.success(f"✅ Likely Legitimate URL\n\nRisk Score: {probability:.2f}%")

st.markdown("---")

# -----------------------------
# SMS SPAM SECTION
# -----------------------------
st.header("📩 SMS Spam Detection")

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def predict_sms(text):
    text = clean_text(text)
    text_vec = vectorizer.transform([text])
    prediction = sms_spam_model.predict(text_vec)[0]
    probability = sms_spam_model.predict_proba(text_vec)[0][1]

    if prediction == 1:
        return f"🚨 SPAM (Confidence: {probability*100:.2f}%)"
    else:
        return f"✅ NOT SPAM (Confidence: {(1-probability)*100:.2f}%)"

input_method = st.radio(
    "Choose Input Method:",
    ("Type SMS manually", "Upload Screenshot Image")
)

if input_method == "Type SMS manually":
    user_text = st.text_area("Enter your SMS message:")
    
    if st.button("Analyze SMS"):
        if user_text.strip() == "":
            st.warning("Please enter an SMS message.")
        else:
            result = predict_sms(user_text)
            st.info(result)

elif input_method == "Upload Screenshot Image":
    uploaded_file = st.file_uploader("Upload an image containing SMS text", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)

        extracted_text = pytesseract.image_to_string(img)

        st.subheader("Extracted Text:")
        st.write(extracted_text)

        result = predict_sms(extracted_text)
        st.info(result)
