from embeddings_client import get_client
from typing import List, Dict, Any

def check_corpus(corpus_texts: List[str]) -> List[Dict[str, Any]]:
    client = get_client()
    safety_results = []
    for text in corpus_texts:
        response = client.moderations.create(input=text)
        result = response.results[0]
        safety_results.append({
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
            "flagged": result.flagged,
            "categories": {k: v for k, v in result.categories.__dict__.items() if v},
            "category_scores": {k: getattr(result.category_scores, k) for k in dir(result.category_scores) if not k.startswith('_')}
        })
    return safety_results