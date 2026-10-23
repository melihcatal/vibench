import os
import cohere


def get_script_embedding(text: str):
    """
    Generates embeddings for a given script using Cohere.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings[0]
