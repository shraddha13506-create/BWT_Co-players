spam_keywords = [
    "free", "win", "winner", "prize", "cash",
    "urgent", "claim", "click", "offer",
    "limited time", "lottery", "call now"
]

def sender_spam_check(message, recipients, model, vectorizer):
    risk_score = 0

    text_vec = vectorizer.transform([message])
    spam_prob = model.predict_proba(text_vec)[0][1]

    if spam_prob > 0.7:
        risk_score += 40

    keyword_hits = 0
    for word in spam_keywords:
        if word.lower() in message.lower():
            keyword_hits += 1

    risk_score += keyword_hits * 10

    if recipients > 5:
        risk_score += 30
    elif recipients > 2:
        risk_score += 15

    print("\n--- Sender Side Analysis ---")
    print(f"Spam Probability: {spam_prob*100:.2f}%")
    print(f"Keyword Matches: {keyword_hits}")
    print(f"Recipients Count: {recipients}")
    print(f"Final Risk Score: {risk_score}")

    if risk_score >= 50:
        print("⛔ MESSAGE BLOCKED (High Spam Risk)")
    else:
        print("✅ Message Allowed")
