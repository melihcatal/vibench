from embeddings_client import get_cohere_client


def embed_text(text: str):
    cohere_client = get_cohere_client()
    response = cohere_client.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings[0]
