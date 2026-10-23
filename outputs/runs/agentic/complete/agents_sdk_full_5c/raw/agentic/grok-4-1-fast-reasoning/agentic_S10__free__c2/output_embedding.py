from model_client import client

def get_output_embedding(text: str) -> list[float]:
    """
    Embed model outputs for clustering or retrieval.
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return [float(x) for x in response.data[0].embedding]