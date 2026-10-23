from model_client import get_model_client, AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME

def embed_text(text: str):
    """
    Generates an embedding for a given text using an Azure OpenAI embedding model.
    
    Args:
        text: The text to embed.
    
    Returns:
        A list of floats representing the embedding vector.
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty.")
        
    client = get_model_client()
    embedding_deployment = AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME

    # Ensure the input is a non-empty string
    text_to_embed = text.replace("\n", " ")

    response = client.embeddings.create(
        model=embedding_deployment, # e.g. "text-embedding-3-small"
        input=text_to_embed
    )

    return response.data[0].embedding
