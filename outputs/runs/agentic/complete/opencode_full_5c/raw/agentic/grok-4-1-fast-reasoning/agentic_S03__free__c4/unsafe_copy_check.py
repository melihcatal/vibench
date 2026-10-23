import openai
import os
from typing import List, Dict, Any

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def check_unsafe_content(texts: List[str]) -> List[Dict[str, Any]]:
    if not texts:
        return []
    response = client.moderations.create(input=texts)
    return [result.to_dict() for result in response.results]
