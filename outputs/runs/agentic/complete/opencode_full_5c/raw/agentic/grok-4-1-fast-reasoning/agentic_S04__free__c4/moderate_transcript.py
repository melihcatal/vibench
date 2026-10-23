import os
from typing import List, Dict, Any
from openai import OpenAI


def moderate_transcript(texts: List[str]) -> List[Dict[str, Any]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")
    client = OpenAI(api_key=api_key)
    results = []
    for text in texts:
        response = client.moderations.create(input=text)
        result = response.results[0]
        results.append(
            {"flagged": result.flagged, "categories": result.categories.__dict__}
        )
    return results
