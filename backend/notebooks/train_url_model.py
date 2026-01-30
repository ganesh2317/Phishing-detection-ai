import pandas as pd
import numpy as np
import pickle
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.app.utils.preprocess import extract_url_features
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def train_url_model():
    print("Loading URL data...")
    try:
        df = pd.read_csv('backend/data/phishing_url_data.csv')
    except FileNotFoundError:
        print("Data file not found.")
        return

    print("Extracting features...")
    # Apply feature extraction
    features_list = df['url'].apply(extract_url_features)
    X = pd.DataFrame(features_list.tolist())
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Random Forest for URLs...")
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"URL Model Accuracy: {acc:.4f}")
    print(classification_report(y_test, preds))

    os.makedirs('backend/app/models', exist_ok=True)
    with open('backend/app/models/phishing_url_model.pkl', 'wb') as f:
        pickle.dump(clf, f)
    print("URL model saved.")

if __name__ == "__main__":
    train_url_model()
