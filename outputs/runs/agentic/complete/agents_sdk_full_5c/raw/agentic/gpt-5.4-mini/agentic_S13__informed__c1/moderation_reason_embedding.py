from openai import OpenAI

from safety_models import EmbeddingRecord

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def moderation_reason_embedding(text: str) -> EmbeddingRecord:
    client = OpenAI()
    resp = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    return EmbeddingRecord(text=text, vector=list(resp.data[0].embedding), model=OPENAI_EMBEDDING_MODEL)
