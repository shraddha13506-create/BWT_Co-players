

# ==========================================
# 📌 1. IMPORT LIBRARIES
# ==========================================

import pandas as pd
import requests
import zipfile
import io
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt
from google.colab import files

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score


# ==========================================
# 📌 2. LOAD REAL SMS DATASET
# ==========================================

print("Loading SMS Dataset...")

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"

response = requests.get(url)
zip_file = zipfile.ZipFile(io.BytesIO(response.content))

with zip_file.open('SMSSpamCollection') as f:
    df_sms = pd.read_csv(f, sep='\t', header=None, names=['label','message'])

df_sms['label'] = df_sms['label'].map({'ham':0, 'spam':1})

print("Dataset Loaded Successfully")
print(df_sms['label'].value_counts())


# ==========================================
# 📌 3. TRAIN SMS MODEL
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    df_sms['message'],
    df_sms['label'],
    test_size=0.2,
    random_state=42
)

vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = MultinomialNB()
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)

print("Model Accuracy:", accuracy_score(y_test, y_pred))


# ==========================================
# 📌 4. PREDICTION FUNCTION
# ==========================================

def predict_sms(text):
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    probability = model.predict_proba(text_vec)[0][1]
    
    if prediction == 1:
        return f"🚨 SPAM (Confidence: {probability*100:.2f}%)"
    else:
        return f"✅ NOT SPAM (Confidence: {(1-probability)*100:.2f}%)"


# ==========================================
# 📌 5. MAIN INTERFACE
# ==========================================

while True:
    
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
        print("\nUpload Screenshot Image")
        uploaded = files.upload()
        
        image_path = list(uploaded.keys())[0]
        img = Image.open(image_path)
        
        plt.imshow(img)
        plt.axis('off')
        plt.show()
        
        extracted_text = pytesseract.image_to_string(img)
        
        print("\nExtracted Text:")
        print(extracted_text)
        
        result = predict_sms(extracted_text)
        print("\nPrediction from Image:", result)
    
    elif choice == "3":
        print("Program Ended.")
        break
    
    else:
        print("Invalid choice. Try again.")


