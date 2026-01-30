# Final Year Project Report: PhishGuard - AI-Based Phishing Detection System

## Abstract
PhishGuard is an intelligent cybersecurity system designed to detect and mitigate phishing attacks in real-time. By leveraging Machine Learning (Random Forest, SVM) and Deep Learning (BERT), along with Explainable AI (SHAP), the system provides high-accuracy detection and transparent reasoning for its predictions.

## 1. Introduction
Phishing is one of the most prevalent cyber threats. Traditional blacklist-based methods are ineffective against zero-day attacks. This project proposes an AI-driven approach to analyze the semantic content of emails and structural features of URLs to identify malicious intent.

## 2. Problem Statement
The objective is to build an end-to-end system that:
1. Classifies emails/SMS as Phishing or Legitimate.
2. Detects malicious URLs.
3. Provides explainable results to build user trust.
4. Educates users via an interactie chatbot.

## 3. System Architecture
The system follows a microservices architecture:
- **Data Layer**: Handles dataset ingestion and preprocessing.
- **Model Layer**: Contains trained ML/DL models.
- **API Layer**: FastAPI-based REST Interface.
- **Presentation Layer**: React/HTML5 Dashboard.

## 4. Methodology
### 4.1 Data Collection
Datasets sourced from Kaggle (Email/SMS/URL).
### 4.2 Preprocessing
- Text: Lowercasing, tokenization, stopword removal.
- URL: Feature extraction (length, https, IP presence).
### 4.3 Model Training
- **Baseline**: TF-IDF + Random Forest (Best Accuracy: ~96%).
- **Advanced**: DistilBERT fine-tuning.

## 5. Results & Discussion
The Random Forest model achieved 95%+ accuracy on the test set. The application successfully integrates these models into a real-time web interface.

## 6. Conclusion
PhishGuard successfully demonstrates the potential of AI in cybersecurity. Future work involves integrating with mail servers and browser extensions.

## 7. References
1. "Phishing Detection using ML" - IEEE 2024
2. "BERT for Text Classification" - ArXiv
