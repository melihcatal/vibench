from model_client import get_embedding_model, get_openai_client
from model_models import EmbeddingResult


def embed_output(text: str) -> EmbeddingResult:
    client = get_openai_client()
    model = get_embedding_model()
    response = client.embeddings.create(
        model=model,
        input=text,
    )
    return EmbeddingResult(
        provider="OpenAI",
        model=model,
        embedding=list(response.data[0].embedding),
    )
