from openai import OpenAI
from typing import Dict
from safety_client import get_openai_api_key
from safety_models import normalize_openai_result, SafetyDecision

def safety_threshold(text: str, category_thresholds: Dict[str, float]) -> bool:
    client = OpenAI(api_key=get_openai_api_key())
    response = client.moderations.create(
        model="text-moderation-latest",
        input=text
    )
    result = response.results[0]
    decision = normalize_openai_result(result)
    return all(decision.categories.get(cat, 0.0) < thresh for cat, thresh in category_thresholds.items())
