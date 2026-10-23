import os
from typing import Dict, Optional
from openai import OpenAI
from translation_models import UnsafeContentCheckResult

def check_unsafe_content(text: str, language: Optional[str] = None) -> UnsafeContentCheckResult:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    response = client.moderations.create(input=text)

    result = response.results[0]
    
    is_unsafe = result.flagged
    categories = {k: v for k, v in result.categories.dict().items()}
    category_scores = {k: v for k, v in result.category_scores.dict().items()}

    return UnsafeContentCheckResult(
        is_unsafe=is_unsafe,
        categories=categories,
        category_scores=category_scores,
    )
