from model_client import get_model_client

def embed_output(text: str) -> list:
    client = get_model_client()
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"  # Concrete OpenAI embedding model identifier
    )
    return response.data[0].embedding