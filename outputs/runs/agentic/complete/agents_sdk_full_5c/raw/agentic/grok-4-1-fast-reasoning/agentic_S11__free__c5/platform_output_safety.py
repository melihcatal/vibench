import openai
import os
from typing import Dict

def check_platform_output_for_unsafe_content(output_text: str) -> Dict:
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    moderation_response = client.moderation.create(
        input=output_text,
        model='text-moderation-latest'
    )
    result = moderation_response.results[0]
    return {
        'flagged': result.flagged,
        'categories': result.categories,
        'category_scores': result.category_scores
    }