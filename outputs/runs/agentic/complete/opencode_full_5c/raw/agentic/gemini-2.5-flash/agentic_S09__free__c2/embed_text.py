from embeddings_client import get_cohere_client, COHERE_MODEL_NAME


def embed_single_text(text: str) -> list[float]:
    co = get_cohere_client()
    response = co.embed(
        texts=[text], model=COHERE_MODEL_NAME, input_type="search_query"
    )
    return response.embeddings[0]
