import os
import openai

from document_client import set_openai_api_key
from document_models import SafetyResponse, SafetyCategoryResult

def check_ocr_text_safety(text: str) -> SafetyResponse:
    set_openai_api_key()

    response = openai.moderations.create(input=text)
    result = response.results[0]

    categories = []
    for category, flagged in result.categories.__dict__.items():
        if not category.startswith('_') and flagged:
            score = getattr(result.category_scores, category)
            categories.append(SafetyCategoryResult(
                category=category,
                severity=int(score * 100), 
                flagged=flagged
            ))

    return SafetyResponse(flagged=result.flagged, categories=categories)
