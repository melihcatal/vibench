import os
from openai import OpenAI

def vendor_text_safety(text: str) -> dict:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.moderations.create(
        input=text,
        model="text-moderation-3.5-turbo"
    )
    return {
        'flagged': response.results[0].flagged,
        'categories': response.results[0].categories,
        'category_scores': response.results[0].category_scores
    }
