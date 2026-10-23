import os
import openai

def moderate_free_text_claim(text: str) -> dict:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = openai.OpenAI(api_key=openai_api_key)
    
    response = client.moderations.create(input=text)
    
    moderation_result = response.results[0]
    return {
        "flagged": moderation_result.flagged,
        "categories": {
            category.name: category.value for category in moderation_result.categories
        },
        "category_scores": {
            score.name: score.value for score in moderation_result.category_scores
        }
    }
