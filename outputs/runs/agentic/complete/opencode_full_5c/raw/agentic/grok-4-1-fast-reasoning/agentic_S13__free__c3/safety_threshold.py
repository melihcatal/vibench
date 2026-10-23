import requests
from typing import Dict
from safety_client import get_api_key
from safety_models import ModerationResult, CategoryScore, normalize_categories

HF_MODEL = "Unitary/toxic-bert"
HF_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"


def safety_threshold(mr: ModerationResult, thresholds: Dict[str, float]) -> bool:
    hf_token = get_api_key("huggingface")
    resp = requests.post(
        HF_URL,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": mr.input_text},
    )
    resp.raise_for_status()
    data = resp.json()
    toxic_prob = data[0][1]["score"]
    mr.scores.append(CategoryScore("toxicity", toxic_prob))
    for score in mr.scores:
        thresh = thresholds.get(score.category, 0.5)
        if score.probability > thresh:
            score.blocked = True
            return False
    return True
