import os
from typing import List, Dict, Any
from openai import OpenAI

def corpus_safety(texts: List[str]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not texts:
        return {"flagged": [], "summary": {"total": 0, "unsafe_count": 0}}
    response = client.moderations.create(
        input=texts,
        model="text-moderation-latest"
    )
    return {
        "flagged": response.results,
        "summary": {
            "total": len(texts),
            "unsafe_count": sum(1 for r in response.results if r.flagged)
        }
    }
