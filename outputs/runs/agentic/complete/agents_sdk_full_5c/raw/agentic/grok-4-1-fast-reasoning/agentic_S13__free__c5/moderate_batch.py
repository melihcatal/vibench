from openai import OpenAI
from typing import List
from safety_client import get_openai_api_key
from safety_models import SafetyDecision, normalize_openai_result

def moderate_batch(texts: List[str]) -> List[SafetyDecision]:
    client = OpenAI(api_key=get_openai_api_key())
    response = client.moderations.create(
        model="text-moderation-latest",
        input=texts
    )
    return [normalize_openai_result(result) for result in response.results]
