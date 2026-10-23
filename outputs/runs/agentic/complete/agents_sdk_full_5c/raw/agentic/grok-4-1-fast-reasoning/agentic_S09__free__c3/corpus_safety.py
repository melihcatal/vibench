import os
from typing import List, Dict, Any
from openai import OpenAI

def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY required")
    return OpenAI(api_key=api_key)

def corpus_safety_check(texts: List[str]) -> Dict[str, Any]:
    client = get_client()
    results = []
    for i, text in enumerate(texts):
        resp = client.moderations.create(input=text)
        result = resp.results[0]
        results.append({
            "index": i,
            "flagged": result.flagged,
            "categories": result.categories,
            "preview": text[:100] + "..." if len(text) > 100 else text
        })
    flagged = [r for r in results if r["flagged"]]
    return {
        "total": len(texts),
        "flagged_count": len(flagged),
        "flagged_ratio": len(flagged) / len(texts) if texts else 0,
        "safe": len(flagged) == 0
    }