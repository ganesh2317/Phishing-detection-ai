import pandas as pd
import numpy as np
import pickle
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.app.utils.preprocess import clean_text
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def train_ml_models():
    print("Loading data...")
    try:
        df = pd.read_csv('backend/data/phishing_text_data.csv')
    except FileNotFoundError:
        print("Data file not found. Please run generate_mock_data.py first.")
        return

    print("Cleaning text...")
    df['cleaned_text'] = df['text'].apply(clean_text)

    X_train, X_test, y_train, y_test = train_test_split(df['cleaned_text'], df['label'], test_size=0.2, random_state=42)

    print("Vectorizing...")
    tfidf = TfidfVectorizer(max_features=5000)
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    models = {
        "Logistic Regression": LogisticRegression(),
        "Naive Bayes": MultinomialNB(),
        "Random Forest": RandomForestClassifier(n_estimators=100),
        "SVM": SVC(probability=True)
    }

    best_model = None
    best_acc = 0
    best_name = ""

    results = {}

    print("Training models...")
    for name, model in models.items():
        model.fit(X_train_tfidf, y_train)
        preds = model.predict(X_test_tfidf)
        acc = accuracy_score(y_test, preds)
        results[name] = acc
        print(f"\n{name} Accuracy: {acc:.4f}")
        print(classification_report(y_test, preds))
        
        if acc > best_acc:
            best_acc = acc
            best_model = model
            best_name = name

    print(f"\nBest Model: {best_name} with Accuracy: {best_acc:.4f}")

    # Save best model and vectorizer
    os.makedirs('backend/app/models', exist_ok=True)
    with open('backend/app/models/phishing_text_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    with open('backend/app/models/tfidf_vectorizer.pkl', 'wb') as f:
        pickle.dump(tfidf, f)
    print("Model saved to backend/app/models/")

if __name__ == "__main__":
    train_ml_models()
