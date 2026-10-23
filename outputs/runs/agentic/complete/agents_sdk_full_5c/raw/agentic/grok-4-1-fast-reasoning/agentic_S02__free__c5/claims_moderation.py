import openai
import os

def moderate_free_text_claims(text: str) -> dict:
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.moderations.create(input=text)
    result = response.results[0]
    return {
        'flagged': result.flagged,
        'categories': result.categories.__dict__ if hasattr(result.categories, '__dict__') else result.categories,
        'category_scores': result.category_scores.__dict__ if hasattr(result.category_scores, '__dict__') else result.category_scores
    }