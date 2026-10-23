from safety_client import get_openai_client, build_embedding_payload
from safety_models import ReasonEmbedding


def moderation_reason_embedding(
    text: str, model: str = "text-embedding-3-small"
) -> ReasonEmbedding:
    client = get_openai_client()
    payload = build_embedding_payload(text, model=model)
    response = client.embeddings.create(**payload)
    embedding = response.data[0].embedding
    return ReasonEmbedding(
        text=text,
        embedding=embedding,
        model=model,
    )
