from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
import os
import sys

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from app.utils.preprocess import clean_text, extract_url_features

app = FastAPI(title="Phishing Detection API", description="API for detecting phishing emails, SMS, and URLs.", version="1.0")

# Load Models
try:
    with open('backend/app/models/phishing_text_model.pkl', 'rb') as f:
        text_model = pickle.load(f)
    with open('backend/app/models/tfidf_vectorizer.pkl', 'rb') as f:
        tfidf_vectorizer = pickle.load(f)
    with open('backend/app/models/phishing_url_model.pkl', 'rb') as f:
        url_model = pickle.load(f)
    print("Models loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")
    text_model = None
    url_model = None

# Request Models
class TextRequest(BaseModel):
    text: str

class UrlRequest(BaseModel):
    url: str

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Phishing Detection API is running."}

@app.post("/predict/text")
def predict_text(request: TextRequest):
    if not text_model:
        # Dummy response for demonstration if model is missing
        return {
            "text": request.text,
            "prediction": "Phishing (Demo)",
            "confidence": 0.99,
            "explanation": "Model not loaded. This is a demo response."
        }
    
    cleaned = clean_text(request.text)
    vectorized = tfidf_vectorizer.transform([cleaned])
    prediction = text_model.predict(vectorized)[0]
    proba = text_model.predict_proba(vectorized)[0]
    
    label = "Phishing" if prediction == 1 else "Legitimate"
    confidence = float(np.max(proba))
    
    return {
        "text": request.text,
        "prediction": label,
        "confidence": confidence,
        "explanation": "SHAP explanation not implemented in baseline." # Placeholder
    }

@app.post("/predict/url")
def predict_url(request: UrlRequest):
    if not url_model:
        # Dummy response
        return {
            "url": request.url,
            "prediction": "Legitimate (Demo)",
            "confidence": 0.85
        }
    
    features = extract_url_features(request.url)
    # Convert features dict to list of values in correct order
    # Keys: 'url_length', 'has_https', 'has_ip', 'num_dots', 'num_slashes', 'has_login'
    # Ensure usage matches training order
    feature_values = [
        features['url_length'], 
        features['has_https'], 
        features['has_ip'], 
        features['num_dots'], 
        features['num_slashes'], 
        features['has_login']
    ]
    
    prediction = url_model.predict([feature_values])[0]
    proba = url_model.predict_proba([feature_values])[0]
    
    label = "Phishing" if prediction == 1 else "Legitimate"
    confidence = float(np.max(proba))
    
    return {
        "url": request.url,
        "prediction": label,
        "confidence": confidence
    }

# Simple Rule-based Chatbot
@app.post("/chat")
def chat(request: ChatRequest):
    user_msg = request.message.lower()
    
    if "phishing" in user_msg:
        response = "Phishing is a type of cyber attack where attackers try to trick you into revealing sensitive information."
    elif "safe" in user_msg or "protect" in user_msg:
        response = "To stay safe, never click on suspicious links, verify the sender, and enable two-factor authentication."
    elif "hello" in user_msg or "hi" in user_msg:
        response = "Hello! I am your cybersecurity assistant. Ask me anything about phishing."
    else:
        response = "I can help you analyze emails and URLs for phishing. Try asking 'What is phishing?'"
        
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
