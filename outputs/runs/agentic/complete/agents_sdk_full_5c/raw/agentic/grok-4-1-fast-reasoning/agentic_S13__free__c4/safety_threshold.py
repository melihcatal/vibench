import requests
from typing import Dict
from safety_client import HF_TOKEN
from safety_models import SafetyResult

HF_MODEL = "unitary/toxic-bert"

def safety_threshold(scores: Dict[str, float], category_thresholds: Dict[str, float]) -> bool:
    # Example with HF for additional toxicity check, but primarily thresholds
    # For demo, check HF toxicity
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": list(scores.keys())[0] if scores else "test"}  # simplistic
    resp = requests.post(f"https://api-inference.huggingface.co/models/{HF_MODEL}", headers=headers, json=payload).json()
    tox_score = resp[0][0]['score'] if resp and len(resp[0]) > 0 else 0.0
    return all(scores.get(cat, 0.0) < category_thresholds.get(cat, 0.5) for cat in scores) and tox_score < 0.5