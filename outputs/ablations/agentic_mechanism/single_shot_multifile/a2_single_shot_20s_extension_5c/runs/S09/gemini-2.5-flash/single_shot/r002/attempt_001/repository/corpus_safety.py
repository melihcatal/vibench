import os
from typing import List, Dict, Any

from openai import OpenAI

def check_corpus_safety(texts: List[str]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    results = []
    for i, text in enumerate(texts):
        response = client.moderations.create(input=text)
        moderation_output = response.results[0]
        results.append({
            "text_index": i,
            "text": text,
            "flagged": moderation_output.flagged,
            "categories": moderation_output.categories.model_dump()
        })
    
    overall_flagged = any(r["flagged"] for r in results)

    return {
        "overall_flagged": overall_flagged,
        "detailed_results": results
    }