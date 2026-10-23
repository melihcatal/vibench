import os
from typing import Dict, List

from embeddings_client import DirectEmbeddingsClient
from embeddings_models import EmbeddingRequest


MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def corpus_safety(texts: List[str]) -> Dict[str, object]:
    client = DirectEmbeddingsClient(base_url=os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1")
    flagged = []
    for text in texts:
        response = client.embed(EmbeddingRequest(model=MODERATION_MODEL, input=text))
        flagged.append({"text": text, "checked": bool(response)})
    return {"provider": "openai", "model": MODERATION_MODEL, "items": flagged}


if __name__ == "__main__":
    import json
    import sys

    payload = json.loads(sys.stdin.read() or "[]")
    print(json.dumps(corpus_safety(payload)))
