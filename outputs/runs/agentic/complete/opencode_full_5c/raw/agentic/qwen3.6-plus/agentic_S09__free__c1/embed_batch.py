from typing import List
from embeddings_client import get_openai_client, get_embedding_model
from embeddings_models import (
    BatchEmbeddingResponse,
    parse_batch_embedding_response,
    normalize_vector,
)


def embed_batch(
    texts: List[str], normalize: bool = False, dimensions: int = None
) -> BatchEmbeddingResponse:
    client = get_openai_client()
    model = get_embedding_model()

    api_response = client.embeddings.create(
        model=model,
        input=texts,
        encoding_format="float",
        dimensions=dimensions,
    )

    result = parse_batch_embedding_response(api_response)

    if normalize:
        for item in result.data:
            item.embedding = normalize_vector(item.embedding)

    return result


if __name__ == "__main__":
    import json

    texts = ["Hello world", "Goodbye world", "Testing embeddings"]
    response = embed_batch(texts)
    output = {
        "model": response.model,
        "usage": response.usage,
        "embeddings": [
            {
                "index": item.index,
                "length": len(item.embedding),
                "first_3": item.embedding[:3],
            }
            for item in response.data
        ],
    }
    print(json.dumps(output, indent=2))
