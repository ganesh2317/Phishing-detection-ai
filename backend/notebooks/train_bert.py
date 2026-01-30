import pandas as pd
import numpy as np
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import sys
import os

# Ensure we can run this script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.app.utils.preprocess import clean_text

class PhishingDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def train_bert_model():
    print("Loading data for BERT...")
    try:
        df = pd.read_csv('backend/data/phishing_text_data.csv')
    except FileNotFoundError:
        print("Data file not found.")
        return

    # Sample data for speed if needed
    df = df.sample(frac=0.5, random_state=42) 
    
    train_texts, val_texts, train_labels, val_labels = train_test_split(df['text'], df['label'], test_size=0.2)

    print("Tokenizing...")
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    train_encodings = tokenizer(train_texts.tolist(), truncation=True, padding=True, max_length=128)
    val_encodings = tokenizer(val_texts.tolist(), truncation=True, padding=True, max_length=128)

    train_dataset = PhishingDataset(train_encodings, train_labels.tolist())
    val_dataset = PhishingDataset(val_encodings, val_labels.tolist())

    training_args = TrainingArguments(
        output_dir='./backend/app/models/bert_results',
        num_train_epochs=1, # Keep it small for demo
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        warmup_steps=50,
        weight_decay=0.01,
        logging_dir='./backend/app/models/logs',
        logging_steps=10,
        eval_strategy="steps", # Updated from evaluation_strategy, or use "epoch"
        save_strategy="no" # Don't save checkpoints to save space
    )

    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )

    print("Training BERT...")
    trainer.train()

    print("Evaluating BERT...")
    eval_results = trainer.evaluate()
    print(eval_results)

    print("Saving BERT model...")
    model.save_pretrained("backend/app/models/phishing_bert")
    tokenizer.save_pretrained("backend/app/models/phishing_bert")

if __name__ == "__main__":
    train_bert_model()
