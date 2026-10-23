import cohere

from model_models import EmbeddingResult, normalize_text


def embed_output(
    text: str, model: str = "embed-v4.0", input_type: str = "search_document"
) -> dict:
    client = cohere.ClientV2()
    response = client.embed(
        model=model,
        input_type=input_type,
        texts=[normalize_text(text)],
        embedding_types=["float"],
    )
    vector = response.embeddings.float_[0]
    result = EmbeddingResult(
        provider="Cohere",
        model=model,
        embedding=vector,
        dimensions=len(vector),
    )
    return {
        "provider": result.provider,
        "model": result.model,
        "embedding": result.embedding,
        "dimensions": result.dimensions,
    }
