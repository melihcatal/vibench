import os
import openai
from typing import Dict, Any

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def moderate_transcript(transcript_text: str) -> Dict[str, Any]:
    response = client.moderations.create(
        input=transcript_text, model="text-moderation-latest"
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
