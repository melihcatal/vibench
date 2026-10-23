from embeddings_client import get_openai_client, get_embedding_model
from embeddings_models import (
    EmbeddingRequest,
    SingleEmbeddingResponse,
    parse_single_embedding_response,
    normalize_vector,
)


def embed_text(
    text: str, normalize: bool = False, dimensions: int = None
) -> SingleEmbeddingResponse:
    client = get_openai_client()
    model = get_embedding_model()

    request = EmbeddingRequest(input=text, model=model, dimensions=dimensions)

    api_response = client.embeddings.create(
        model=request.model,
        input=request.input,
        encoding_format=request.encoding_format,
        dimensions=request.dimensions,
    )

    result = parse_single_embedding_response(api_response)

    if normalize:
        result.embedding = normalize_vector(result.embedding)

    return result


if __name__ == "__main__":
    import json

    response = embed_text("Hello, world!")
    print(
        json.dumps(
            {
                "index": response.index,
                "embedding_length": len(response.embedding),
                "first_5_values": response.embedding[:5],
            },
            indent=2,
        )
    )
