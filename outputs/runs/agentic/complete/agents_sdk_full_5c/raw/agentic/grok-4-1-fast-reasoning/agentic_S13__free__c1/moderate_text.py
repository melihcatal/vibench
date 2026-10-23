from safety_client import openai_client
from safety_models import SafetyResult, normalize_openai

def moderate_text(text: str) -> SafetyResult:
    client = openai_client()
    raw_response = client.moderations.create(
        input=text,
        model="text-moderation-latest"
    )
    return normalize_openai(raw_response, text)