import os
import json
from typing import Dict, Any, List
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def record_text_safety(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = []
    for doc in documents:
        texts = [str(v) for v in doc.values() if isinstance(v, str) and len(str(v)) > 10]
        text = ' '.join(texts[:5])  # limit
        if not text:
            results.append({'flagged': False})
            continue
        response = client.moderations.create(
            input=text,
            model="text-moderation-latest"
        )
        result = response.results[0]
        results.append({
            'document_id': doc.get('id', 'unknown'),
            'flagged': result.flagged,
            'categories': result.categories,
            'category_scores': result.category_scores
        })
    return results
