import os
from typing import List, Dict, Any

from google.cloud import aiplatform

def embed_metadata_and_text(metadata: Dict[str, Any], extracted_text: str) -> List[float]:
    """
    Embeds object metadata and extracted text using Google Cloud Vertex AI's textembedding-gecko model.

    Args:
        metadata: A dictionary containing object metadata.
        extracted_text: The text extracted from the object.

    Returns:
        A list of floats representing the embedding vector.
    """
    aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_REGION"))

    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko")
    
    # Combine metadata (as a string) and extracted text for embedding
    metadata_string = str(metadata)
    combined_text = f"Metadata: {metadata_string}
Extracted Text: {extracted_text}"

    embeddings = model.get_embeddings([combined_text])
    return embeddings[0].values

