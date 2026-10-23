import os
import openai
from model_client import get_openai_client

def check_safety(text: str) -> dict:
    client = get_openai_client()
    
    response = client.moderations.create(input=text)
    
    moderation_result = response.results[0]
    
    return {
        "flagged": moderation_result.flagged,
        "categories": {
            category: score 
            for category, score in moderation_result.category_scores.model_dump().items()
        },
        "category_flags": {
            category: flag 
            for category, flag in moderation_result.categories.model_dump().items()
        }
    }
