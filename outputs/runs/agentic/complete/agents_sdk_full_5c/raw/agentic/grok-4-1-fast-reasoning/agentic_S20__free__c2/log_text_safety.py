import os
from typing import List, Dict, Any
from openai import OpenAI

def log_text_safety(log_texts: List[str]) -> List[Dict[str, Any]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    results = []
    for text in log_texts:
        moderation = client.moderations.create(input=text)
        result = moderation.results[0]
        results.append({
            "input": text[:100] + "..." if len(text) > 100 else text,
            "flagged": result.flagged,
            "categories": {cat: score for cat, score in result.categories.items()},
            "category_scores": {cat: score for cat, score in result.category_scores.items()}
        })
    return results
