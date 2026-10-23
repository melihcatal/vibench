from openai import OpenAI
from vision_client import get_openai_api_key

def visual_safety_text(text_content: str) -> dict:
    api_key = get_openai_api_key()
    client = OpenAI(api_key=api_key)
    response = client.moderations.create(
        input=text_content,
        model="text-moderation-007"
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores)
    }