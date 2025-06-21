import pickle
import pandas as pd

def detect_anomaly(username, ip_address):
    try:
        with open('app/ai/model/model.pkl', 'rb') as f:
            model = pickle.load(f)

        data = pd.DataFrame([{
            'username': username,
            'ip_address': ip_address
        }])
        data['ip_encoded'] = data['ip_address'].astype('category').cat.codes
        data['user_encoded'] = data['username'].astype('category').cat.codes
        features = data[['ip_encoded', 'user_encoded']]

        prediction = model.predict(features)
        return prediction[0] == -1  # -1 means anomaly
    except Exception as e:
        print(f"[ERROR] Detection failed: {e}")
        return False
