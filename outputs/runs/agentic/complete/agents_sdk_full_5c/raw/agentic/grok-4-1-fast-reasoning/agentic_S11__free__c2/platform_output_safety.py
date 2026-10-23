import openai
from typing import Dict, Any

def check_platform_output_safety(text: str) -> Dict[str, Any]:
    client = openai.OpenAI()
    response = client.moderations.create(
        input=text,
        model="text-moderation-latest"
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories.dict(),
        "category_scores": result.category_scores.dict(),
    }