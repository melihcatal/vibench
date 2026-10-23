import os
from openai import OpenAI

def embed_moderation_rationales(rationales: list[str]) -> list[list[float]]:
    """
    Embeds moderation rationales for case retrieval using OpenAI embeddings.
    
    Args:
        rationales (list[str]): A list of strings, where each string is a moderation rationale.
                                
    Returns:
        list[list[float]]: A list of embedding vectors, where each vector corresponds to a rationale.
    """
    # OpenAI API key is typically read from the OPENAI_API_KEY environment variable.
    # If using Azure OpenAI, additional environment variables like AZURE_OPENAI_ENDPOINT
    # and AZURE_OPENAI_API_VERSION would be needed, and the client initialized differently.
    # For this task, assuming standard OpenAI API.
    client = OpenAI()

    # The embedding model to use. 'text-embedding-ada-002' is a common choice.
    # For newer models, check OpenAI documentation.
    model_id = "text-embedding-ada-002"

    embeddings = []
    for rationale in rationales:
        response = client.embeddings.create(input=[rationale], model=model_id)
        # The response structure contains a list of data objects, each with an embedding.
        # We extract the embedding (list of floats) from the first (and only) item.
        embeddings.append(response.data[0].embedding)

    return embeddings
