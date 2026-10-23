from openai import OpenAI

from embeddings_client import get_openai_embeddings_client


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def corpus_safety(texts):
    client: OpenAI = get_openai_embeddings_client()
    results = []
    for text in texts:
        moderation = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
        flagged = moderation.results[0].flagged
        results.append({"text": text, "flagged": flagged, "provider": "openai"})
    return results
