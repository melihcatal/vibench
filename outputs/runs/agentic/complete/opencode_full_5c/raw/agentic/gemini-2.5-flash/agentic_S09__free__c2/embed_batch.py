from embeddings_client import get_cohere_client, COHERE_MODEL_NAME


def embed_batch_texts(texts: list[str]) -> list[list[float]]:
    co = get_cohere_client()
    response = co.embed(
        texts=texts, model=COHERE_MODEL_NAME, input_type="search_document"
    )
    return response.embeddings
