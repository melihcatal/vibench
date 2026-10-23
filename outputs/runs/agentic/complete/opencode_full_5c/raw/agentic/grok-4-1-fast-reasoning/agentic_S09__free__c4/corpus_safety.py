from typing import List
from embeddings_client import get_openai_client


def corpus_safety(corpus: List[str]) -> List[bool]:
    client = get_openai_client()
    results = []
    for text in corpus:
        moderation = client.moderations.create(input=text)
        is_safe = not moderation.results[0].flagged
        results.append(is_safe)
    return results
