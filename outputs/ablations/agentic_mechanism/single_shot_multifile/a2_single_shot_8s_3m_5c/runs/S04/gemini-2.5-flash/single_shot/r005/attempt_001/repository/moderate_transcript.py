import os
from typing import List, Dict
import openai

# OpenAI Configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

def moderate_text_segments(text_segments: List[str]) -> List[Dict]:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    openai.api_key = OPENAI_API_KEY
    moderation_results = []
    for text in text_segments:
        response = openai.moderations.create(
            input=text,
            model="text-moderation-latest"
        )
        moderation_results.append({
            'text': text,
            'moderation_result': response.results[0].model_dump()
        })
    return moderation_results