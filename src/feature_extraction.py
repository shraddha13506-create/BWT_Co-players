import re

def extract_features(url, message_text):
    features = {}

    # URL-based features
    features["url_length"] = len(url)
    features["has_https"] = 1 if "https" in url else 0
    features["dot_count"] = url.count(".")
    features["hyphen_count"] = url.count("-")
    features["has_ip"] = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0

    # Message-based features
    suspicious_keywords = ["verify", "urgent", "login", "update", "bank", "account"]
    features["keyword_flag"] = 1 if any(word in message_text.lower() for word in suspicious_keywords) else 0

    return features
