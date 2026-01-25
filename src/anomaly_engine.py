import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from huggingface_hub import InferenceClient
import os

# Constants
HF_TOKEN = os.environ.get("HF_TOKEN")
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"

class AnomalyEngine:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)

    def generate_sample_data(self):
        np.random.seed(42)
        rows = 100
        time = pd.date_range(start="2024-01-01", periods=rows, freq="H")
        temp = 80 + np.random.normal(0, 2, rows)
        press = 150 + np.random.normal(0, 5, rows)
        vib = 1.2 + np.random.normal(0, 0.1, rows)
        
        # Add an anomaly
        temp[85] = 115
        press[85] = 210
        vib[85] = 3.5
        
        return pd.DataFrame({
            "timestamp": time,
            "temperature": temp,
            "pressure": press,
            "vibration": vib
        })

    def detect_anomalies(self, df):
        features = df[["temperature", "pressure", "vibration"]]
        df["anomaly_score"] = self.model.fit_predict(features)
        df["is_anomaly"] = df["anomaly_score"] == -1
        return df

    def analyze_root_cause(self, anomaly_data):
        prompt = f"""You are a Senior Reliability Engineer. Analyze this anomalous sensor reading and provide a potential root cause analysis.

DATA:
{anomaly_data.to_string()}

ROOT CAUSE ANALYSIS:"""

        response = self.client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content

anomaly_engine = AnomalyEngine()
