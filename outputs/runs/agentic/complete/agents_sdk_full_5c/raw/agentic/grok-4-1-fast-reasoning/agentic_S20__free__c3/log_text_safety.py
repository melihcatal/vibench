import openai
import os

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def check_log_text_safety(text: str) -> dict:
    response = client.moderations.create(
        model="text-moderation-latest",
        input=text
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores)
    }
