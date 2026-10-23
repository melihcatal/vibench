import google.generativeai as genai
import os

def embed_caption_chunks(caption_chunks: list[str]) -> list[list[float]]:
    """
    Embeds caption chunks using a Google Cloud Generative AI embedding model.

    Args:
        caption_chunks: A list of string caption chunks.

    Returns:
        A list of embedding vectors, where each vector is a list of floats.
    """
    # Configure the API key. In a real application, use a secure method for API key management.
    # For demonstration, it's assumed the API key is set as an environment variable.
    # genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Use a specific embedding model from Google Cloud
    model_name = "models/embedding-001"

    embeddings = []
    for chunk in caption_chunks:
        response = genai.embed_content(
            model=model_name,
            content=chunk,
            task_type="SEMANTIC_SIMILARITY"
        )
        embeddings.append(response['embedding'])
    return embeddings

