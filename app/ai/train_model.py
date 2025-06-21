import pandas as pd
from sklearn.ensemble import IsolationForest
import pickle
import os

def generate_dummy_data():
    data = {
        'username': ['admin', 'admin', 'admin', 'user1', 'user1', 'hacker'],
        'ip_address': ['192.168.1.10', '192.168.1.11', '192.168.1.10',
                       '192.168.1.12', '192.168.1.12', '45.67.89.123'],
        'timestamp': pd.date_range(start='2023-01-01', periods=6, freq='D')
    }
    df = pd.DataFrame(data)
    return df

def preprocess(df):
    df['ip_encoded'] = df['ip_address'].astype('category').cat.codes
    df['user_encoded'] = df['username'].astype('category').cat.codes
    return df[['ip_encoded', 'user_encoded']]

def train_and_save_model():
    df = generate_dummy_data()
    X = preprocess(df)

    model = IsolationForest(contamination=0.2, random_state=42)
    model.fit(X)

    os.makedirs('app/ai/model', exist_ok=True)
    with open('app/ai/model/model.pkl', 'wb') as f:
        pickle.dump(model, f)

    print("✅ Model trained and saved.")

if __name__ == '__main__':
    train_and_save_model()