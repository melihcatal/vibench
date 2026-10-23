from typing import Dict, Any
from openai import OpenAI
from model_client import OPENAI_API_KEY
from model_models import ModerationResult

def check_prompt_safety(text: str) -> Dict[str, Any]:
    \"\"\"Check prompts and generated text for unsafe content using OpenAI Moderation.\"\"
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.moderations.create(input=text)
    result = response.results[0]
    return {
        'safe': not result.flagged,
        'categories': result.categories,
        'category_scores': result.category_scores
    }
