import os
from typing import Dict, Any, List
from translation_client import get_openai_client
from translation_models import create_moderation_result

def check_unsafe_content(text: str) -> Dict[str, Any]:
    client = get_openai_client()

    response = client.moderations.create(
        input=text
    )

    moderation_output = response.results[0]
    
    return create_moderation_result(
        text=text,
        flagged=moderation_output.flagged,
        categories=moderation_output.categories.model_dump(),
        category_scores=moderation_output.category_scores.model_dump()
    )
