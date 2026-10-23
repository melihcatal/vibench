import os
from typing import List, Dict, Any
from openai import OpenAI
from vision_models import LabelDetectionResponse

def check_unsafe_text(labels: List[str]) -> Dict[str, Any]:
    """Checks generated visual labels for unsafe text using OpenAI's Moderation API."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    response = client.moderations.create(input=labels)
    results = response.results[0]
    
    return {
        "flagged": results.flagged,
        "categories": results.categories.dict(),
        "category_scores": results.category_scores.dict()
    }

def visual_safety_text(labels: LabelDetectionResponse) -> Dict[str, Any]:
    """Checks visual labels for unsafe text content."""
    safety_check = check_unsafe_text(labels.labels)
    
    return {
        "provider": labels.provider,
        "labels": labels.labels,
        "safety_check": safety_check
    }