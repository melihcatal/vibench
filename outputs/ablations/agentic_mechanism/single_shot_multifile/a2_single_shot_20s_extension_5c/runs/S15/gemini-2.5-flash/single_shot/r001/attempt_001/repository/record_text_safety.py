import os
from typing import Dict, Any
from openai import OpenAI
from database_models import Document

def record_text_safety(document: Document) -> Dict[str, Any]:
    """
    Checks user-generated document fields for unsafe content using OpenAI Moderation API.
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=openai_api_key)

    text_to_moderate = f"Title: {document.title}\nContent: {document.content}"

    response = client.moderations.create(
        input=text_to_moderate,
        model="text-moderation-latest"
    )

    moderation_result = response.results[0]
    
    return {
        "flagged": moderation_result.flagged,
        "categories": moderation_result.categories.model_dump(),
        "category_scores": moderation_result.category_scores.model_dump()
    }
