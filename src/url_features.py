import re
import numpy as np

def extract_features(url):
    url_length = len(url)
    num_dots = url.count(".")
    has_ip = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0
    has_at = 1 if "@" in url else 0

    return np.array([[url_length, num_dots, has_ip, has_at]])
