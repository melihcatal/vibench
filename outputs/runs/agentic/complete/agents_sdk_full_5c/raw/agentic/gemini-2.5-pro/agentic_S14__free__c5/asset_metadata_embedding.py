import os
import json
from typing import List, Dict, Any
from openai import OpenAI

from storage_models import ObjectMetadata

def create_embedding_from_metadata(
    metadata: ObjectMetadata,
    extracted_text: str
) -> List[float] | None:
    """
    Embeds object metadata and extracted text using OpenAI's API.

    This function requires the OPENAI_API_KEY environment variable to be set.

    Args:
        metadata: An ObjectMetadata object for the asset.
        extracted_text: Text content extracted from the asset (e.g., via OCR).

    Returns:
        A list of floats representing the embedding vector, or None on failure.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return None
        
    client = OpenAI(api_key=api_key)

    # Combine metadata and text into a single document for embedding
    combined_content = {
        "key": metadata.key,
        "content_type": metadata.content_type,
        "size_bytes": metadata.content_length,
        "custom_metadata": metadata.metadata or {},
        "extracted_text": extracted_text[:4096] # Truncate to a reasonable limit
    }
    
    input_text = json.dumps(combined_content, indent=2)

    try:
        response = client.embeddings.create(
            model="text-embedding-3-small", # Provider-specific model ID
            input=input_text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error calling OpenAI Embeddings API: {e}")
        return None

# Example Usage
# if __name__ == '__main__':
#     from datetime import datetime
#     # 1. Mock metadata for an object
#     mock_meta = ObjectMetadata(
#         key="financial/report-q3-2023.pdf",
#         content_length=1024 * 512,
#         content_type="application/pdf",
#         last_modified=datetime.utcnow(),
#         etag="a1b2c3d4e5f6",
#         metadata={"department": "finance", "confidentiality": "high"}
#     )
    
#     # 2. Mock text extracted from the object
#     mock_text = "Q3 earnings exceeded expectations, with a 15% year-over-year growth."
    
#     # 3. Generate the embedding
#     embedding_vector = create_embedding_from_metadata(mock_meta, mock_text)
    
#     if embedding_vector:
#         print(f"Successfully created embedding vector with dimension: {len(embedding_vector)}")
#         print(f"First 5 dimensions: {embedding_vector[:5]}")
