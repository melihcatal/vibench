import openai
from safety_client import OPENAI_API_KEY
from safety_models import SafetyResult
from typing import Dict

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def moderate_text(text: str) -> SafetyResult:
    response = client.moderations.create(
        input=text,
        model="text-moderation-latest"
    )
    result = response.results[0]
    categories = {cat.category: cat.relevance_score for cat in result.categories}
    flagged = result.flagged
    severity = max([cat.relevance_score for cat in result.categories], default=0.0)
    return SafetyResult(text, categories, flagged, severity)