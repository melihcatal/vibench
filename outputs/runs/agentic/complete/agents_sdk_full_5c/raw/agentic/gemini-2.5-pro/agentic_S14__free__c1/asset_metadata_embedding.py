import os
from openai import OpenAI
from storage_models import EmbeddingResult, ObjectMetadata

def embed_metadata_and_text_openai(
    metadata: ObjectMetadata,
    extracted_text: str
) -> EmbeddingResult:
    """
    Combines object metadata and extracted text, then generates an embedding
    using the OpenAI Embeddings API.

    Requires the OPENAI_API_KEY environment variable to be set.

    Args:
        metadata (ObjectMetadata): The metadata of the stored object.
        extracted_text (str): The text content extracted from the object (e.g., via OCR).

    Returns:
        An EmbeddingResult containing the vector.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Combine metadata and text into a single document for embedding
    combined_text = (
        f"Document Name: {metadata.name}\n"
        f"Content Type: {metadata.content_type}\n"
        f"Size: {metadata.size} bytes\n"
        f"Last Modified: {metadata.updated.isoformat()}\n\n"
        f"Content:\n{extracted_text}"
    )

    # Use a specific, recommended OpenAI embedding model
    embedding_model = "text-embedding-3-small"

    response = client.embeddings.create(
        input=[combined_text],
        model=embedding_model
    )

    embedding_vector = response.data[0].embedding

    return EmbeddingResult(
        model=embedding_model,
        embedding=embedding_vector,
        source_text=combined_text
    )
