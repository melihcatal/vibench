from typing import List, Dict, Any
from embeddings_client import get_client


def check_corpus_safety(texts: List[str]) -> Dict[str, Any]:
    client = get_client()
    safety_results = []
    for text in texts:
        response = client.moderations.create(input=text)
        safety_results.append(response.results[0])
    flagged = any(r.flagged for r in safety_results)
    return {"flagged": flagged, "num_texts": len(texts), "details": safety_results}
