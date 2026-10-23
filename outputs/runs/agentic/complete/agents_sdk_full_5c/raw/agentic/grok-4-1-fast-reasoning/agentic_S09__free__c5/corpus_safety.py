import os
from typing import List, Dict, Any
from openai import OpenAI

def corpus_safety(corpus_texts: List[str]) -> List[Dict[str, Any]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    safety_results = []
    for text in corpus_texts:
        response = client.moderations.create(
            input=text,
            model="text-moderation-latest"
        )
        flagged = response.results[0].flagged
        safety_results.append({
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
            "safe": not flagged,
            "categories": response.results[0].categories if flagged else None
        })
    
    return safety_results