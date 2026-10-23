import os
from typing import List, Dict, Any
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def corpus_safety(texts: List[str]) -> Dict[str, Any]:
    response = client.moderations.create(model="text-moderation-latest", input=texts)
    flagged_count = sum(1 for r in response.results if r.flagged)
    return {
        "results": response.results,
        "flagged_count": flagged_count,
        "is_safe": flagged_count == 0,
        "total_texts": len(texts),
    }
