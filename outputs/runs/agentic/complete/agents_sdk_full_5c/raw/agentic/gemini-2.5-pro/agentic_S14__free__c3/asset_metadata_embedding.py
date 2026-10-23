import os
from openai import OpenAI
from . import storage_models

def create_metadata_embedding(
    metadata: storage_models.ObjectMetadata, 
    extracted_text: str
) -> storage_models.EmbeddingResult:
    """
    Combines object metadata and extracted text to create an embedding
    using OpenAI's API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Combine metadata and text into a single string for embedding
    combined_text = (
        f"Object Name: {metadata.name}\n"
        f"Content Type: {metadata.content_type}\n"
        f"Size: {metadata.size} bytes\n"
        f"Content:\n{extracted_text}"
    )
    
    embedding_model = "text-embedding-3-small"

    response = client.embeddings.create(
        input=combined_text,
        model=embedding_model
    )

    embedding_vector = response.data[0].embedding

    return storage_models.EmbeddingResult(
        source_text=combined_text,
        embedding_vector=embedding_vector,
        model_id=embedding_model
    )
