import os
import google.generativeai as genai
from storage_models import ObjectMetadata, EmbeddingResult
from typing import Union, List

def embed_metadata_and_text(
    metadata: ObjectMetadata,
    extracted_text: str
) -> EmbeddingResult:
    """
    Creates a combined text from metadata and content, then generates an embedding
    using the Google Gemini embeddings API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    
    # Construct a single text block for embedding
    combined_content = (
        f"Object Name: {metadata.name}\n"
        f"Content Type: {metadata.content_type}\n"
        f"Size: {metadata.size} bytes\n"
        f"---Extracted Text---\n"
        f"{extracted_text}"
    )

    # Use a specific embedding model from the Gemini family
    model_name = "models/text-embedding-004"
    
    result = genai.embed_content(
        model=model_name,
        content=combined_content,
        task_type="RETRIEVAL_DOCUMENT",
        title=f"Embedding for {metadata.name}"
    )

    embedding_vector = result['embedding']
    print(f"Generated embedding for {metadata.name} with vector size {len(embedding_vector)}")
    
    return EmbeddingResult(
        source_content=combined_content,
        embedding=embedding_vector
    )
