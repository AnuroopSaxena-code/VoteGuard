import requests

BACKEND_URL = "http://127.0.0.1:8000"  # update when deployed

def health_check():
    return requests.get(f"{BACKEND_URL}/health").json()

def predict_fraud(file):
    files = {"file": file}
    r = requests.post(f"{BACKEND_URL}/predict-fraud", files=files)
    return r.json()

def predict_news(text):
    r = requests.post(f"{BACKEND_URL}/predict-news", json={"text": text})
    return r.json()
