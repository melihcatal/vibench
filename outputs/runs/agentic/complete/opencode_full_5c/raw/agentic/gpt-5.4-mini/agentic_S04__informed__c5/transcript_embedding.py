from openai import OpenAI

from speech_models import EmbeddingRequest


def transcript_embedding(segments):
    client = OpenAI()
    texts = [segment.get("text", "") for segment in segments or []]
    resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return {"vectors": [item.embedding for item in resp.data], "count": len(resp.data)}
