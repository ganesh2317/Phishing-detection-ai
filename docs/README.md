# PhishGuard - AI-Based Phishing Detection System

## Overview
PhishGuard is an advanced AI-powered system designed to detect phishing attempts in Emails, SMS, and URLs. It utilizes Machine Learning (Logistic Regression, Random Forest) and Deep Learning (BERT) models to classify content as Phishing or Legitimate. The system includes Explainable AI (SHAP) to provide transparency in predictions and a cybersecurity chatbot for user education.

## Architecture
- **Frontend**: Glassmorphism Dashboard (HTML/CSS/JS)
- **Backend**: FastAPI (Python)
- **AI Engine**: Scikit-Learn (Baseline), Transformers (BERT)
- **Data**: Mock datasets generated for Email/SMS and URLs

## Features
- **Email/SMS Analysis**: Detects phishing in text messages.
- **URL Analysis**: Identifies malicious websites based on URL features.
- **Explainability**: (Planned) Visual highlights of suspicious words.
- **Chatbot**: Educational assistant for cybersecurity queries.
- **Real-time API**: Fast and scalable REST API.

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js (Optional for advanced frontend extensions)
- Docker (Optional)

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python notebooks/train_ml.py  # Train ML models
python notebooks/train_url_model.py # Train URL model
uvicorn app.main:app --reload
```

### 2. Frontend Setup
Open `frontend/index.html` in your browser.

## Project Structure
```
/phishing-detection-app
  /backend
    /app
      /api
      /models
      /services
      /utils
    /data
    /notebooks
  /frontend
  /deployment
  /docs
```

## Usage
1. Open the dashboard.
2. Select "Email Scanner" or "URL Scanner".
3. Enter the text/URL and click Scan.
4. View the prediction and confidence score.

## Future Scope
- Integration with email clients (Outlook/Gmail Plugin).
- Real-time browser extension.
- Advanced deep learning model (LSTM/BiLSTM).
