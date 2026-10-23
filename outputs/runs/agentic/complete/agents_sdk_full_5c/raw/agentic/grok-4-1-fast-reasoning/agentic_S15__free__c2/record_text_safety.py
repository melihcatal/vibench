import os
from openai import OpenAI
from typing import Dict, Any

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def check_document_safety(document: Dict[str, Any]) -> bool:
    texts = [str(value) for value in document.values() if isinstance(value, (str, dict)) and len(str(value)) > 0]
    if not texts:
        return True
    combined_text = ' '.join(texts[:10])  # limit to avoid token issues
    response = client.moderations.create(
        model="text-moderation-latest",
        input=combined_text
    )
    result = response.results[0]
    return not result.flagged