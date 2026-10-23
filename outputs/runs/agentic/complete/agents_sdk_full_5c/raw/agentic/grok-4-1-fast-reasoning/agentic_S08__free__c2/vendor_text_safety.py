import os
from openai import OpenAI

def check_vendor_text_safety(vendor_text: str) -> dict:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.moderations.create(
        input=vendor_text
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores)
    }
