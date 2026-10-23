import os
from google.cloud import aiplatform

def get_text_embedding(text: str) -> list[float]:
    """Generates an embedding for the given text using Vertex AI."""
    # Initialize Vertex AI
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # authenticate using `gcloud auth application-default login`
    aiplatform.init(project=os.getenv("GCP_PROJECT_ID"), location=os.getenv("GCP_REGION"))

    # Specify the embedding model
    # "text-embedding-004" is a general-purpose text embedding model.
    # For more specialized use cases, other models like "gecko" might be considered.
    model = aiplatform.language_models.TextEmbeddingModel.from_pretrained("text-embedding-004")

    # Generate the embedding
    embeddings = model.get_embeddings([text])
    return embeddings[0].values

def embed_asset_metadata(metadata: dict, extracted_text: str) -> list[float]:
    """
    Combines asset metadata and extracted text, then generates a single embedding.
    
    Args:
        metadata (dict): A dictionary containing the asset's metadata (e.g., {"title": "Document A", "author": "John Doe"}).
        extracted_text (str): The extracted text content of the asset.
        
    Returns:
        list[float]: The embedding vector for the combined content.
    """
    
    # Combine metadata and text into a single string for embedding
    metadata_string = " ".join([f"{k}: {v}" for k, v in metadata.items()])
    combined_content = f"Metadata: {metadata_string}. Content: {extracted_text}"
    
    # Generate the embedding using the helper function
    embedding = get_text_embedding(combined_content)
    
    return embedding

