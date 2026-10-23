from openai import OpenAI
from safety_client import get_openai_api_key
from safety_models import SafetyDecision, normalize_openai_result

def moderate_text(text: str) -> SafetyDecision:
    client = OpenAI(api_key=get_openai_api_key())
    response = client.moderations.create(
        model="text-moderation-latest",
        input=text
    )
    result = response.results[0]
    return normalize_openai_result(result)
