import pandas as pd
import numpy as np
import os

# Ensure data directory exists
os.makedirs('backend/data', exist_ok=True)

# 1. Generate Mock Email/SMS Data
def generate_text_data(n_samples=1000):
    phishing_templates = [
        "Urgent: Your account {account} has been compromised. Click here {link} to reset.",
        "Congratulations! You won a {prize}. Claim it at {link}.",
        "Dear user, verify your KYC at {link} to avoid suspension.",
        "Bank Alert: Unauthorized transaction of ${amount} detected. Review: {link}"
    ]
    
    legit_templates = [
        "Meeting reminder: Project sync at {time}.",
        "Your order #{order_id} has been shipped.",
        "Hi, are we still on for lunch?",
        "Security Alert: specific login detected from new device."
    ]
    
    data = []
    
    for _ in range(n_samples):
        label = np.random.choice([0, 1]) # 0: Legit, 1: Phishing
        
        if label == 1:
            template = np.random.choice(phishing_templates)
            text = template.format(
                account="XYZ Bank",
                link="http://bit.ly/fake",
                prize="iPhone 15",
                amount="500",
                time="10:00 AM",
                order_id="12345"
            )
        else:
            template = np.random.choice(legit_templates)
            text = template.format(
                time="2:00 PM",
                order_id=np.random.randint(1000, 9999)
            )
            
        data.append({'text': text, 'label': label})
        
    df = pd.DataFrame(data)
    df.to_csv('backend/data/phishing_text_data.csv', index=False)
    print("Generated backend/data/phishing_text_data.csv")

# 2. Generate Mock URL Data
def generate_url_data(n_samples=1000):
    phishing_domains = ['secure-login.com', 'update-bank.net', 'apple-verify.xyz', 'paypal-secure.info']
    legit_domains = ['google.com', 'facebook.com', 'amazon.com', 'nytimes.com']
    
    data = []
    for _ in range(n_samples):
        label = np.random.choice([0, 1])
        if label == 1:
            domain = np.random.choice(phishing_domains)
            url = f"http://{domain}/login.php?user={np.random.randint(1000,9999)}"
        else:
            domain = np.random.choice(legit_domains)
            url = f"https://www.{domain}/news/article"
            
        data.append({'url': url, 'label': label})
        
    df = pd.DataFrame(data)
    df.to_csv('backend/data/phishing_url_data.csv', index=False)
    print("Generated backend/data/phishing_url_data.csv")

if __name__ == "__main__":
    generate_text_data()
    generate_url_data()
