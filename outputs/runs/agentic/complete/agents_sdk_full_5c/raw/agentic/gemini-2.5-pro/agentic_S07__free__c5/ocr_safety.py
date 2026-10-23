# ocr_safety.py
import os
from openai import OpenAI
from typing import List
from document_models import SafetyRating

def check_text_safety(text: str) -> List[SafetyRating]:
    """
    Checks text for unsafe content using the OpenAI Moderation API.
    
    Requires OPENAI_API_KEY environment variable to be set.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.moderations.create(input=text)
    
    results = response.results[0]
    
    ratings = []
    for category, flagged in results.categories:
        score = results.category_scores.__getattribute__(category)
        ratings.append(SafetyRating(category=category, is_flagged=flagged, score=score))
        
    return ratings
