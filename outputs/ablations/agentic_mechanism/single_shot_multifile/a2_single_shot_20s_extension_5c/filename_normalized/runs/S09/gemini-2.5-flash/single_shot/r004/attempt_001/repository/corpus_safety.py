import os
import openai
from typing import Dict, Any

def check_corpus_safety(text: str) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        input=text,
        model="text-moderation-latest"
    )
    return response.results[0].model_dump()
