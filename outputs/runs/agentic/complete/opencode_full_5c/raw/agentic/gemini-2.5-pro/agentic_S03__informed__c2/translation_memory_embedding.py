import os
import cohere


def get_translation_embedding(text: str):
    """
    Generates an embedding for a text segment using Cohere.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    co = cohere.Client(api_key)

    response = co.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )

    return response.embeddings[0]
