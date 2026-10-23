import os
import requests
from typing import List, Dict, Any

API_KEY = os.getenv("PERSPECTIVE_API_KEY")
BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_text_safety(text: str) -> Dict:
    url = f"{BASE_URL}?key={API_KEY}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def check_documents_safety(documents: List[Dict[str, Any]]) -> List[Dict]:
    safety_results = []
    for doc in documents:
        texts = [v for v in doc.values() if isinstance(v, str) and len(str(v)) > 20]
        doc_results = [check_text_safety(t) for t in texts]
        safety_results.append(
            {
                "document": doc["id"] if "id" in doc else "unknown",
                "fields_safety": doc_results,
            }
        )
    return safety_results
