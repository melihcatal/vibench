import requests
from typing import List, Dict, Any
from safety_models import SafetyCategory, ModerationDecision, BatchModerationDecision
from safety_client import get_api_key

MODEL_ID = "unitary/toxic-bert"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"


def moderate_batch(texts: List[str]) -> Dict[str, Any]:
    token = get_api_key("HF_TOKEN")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": texts}
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    hf_results = response.json()
    decisions = []
    for i, text in enumerate(texts):
        res = hf_results[i]
        toxic_score = 0.0
        if isinstance(res, list):
            toxic_scores = [r["score"] for r in res if r["label"] == "LABEL_1"]
            toxic_score = toxic_scores[0] if toxic_scores else 0.0
        categories = [{"category": "toxicity", "score": toxic_score}]
        flagged = toxic_score > 0.5
        decisions.append(
            {
                "input_text": text,
                "flagged": flagged,
                "categories": categories,
                "details": None,
            }
        )
    return {"decisions": decisions}
