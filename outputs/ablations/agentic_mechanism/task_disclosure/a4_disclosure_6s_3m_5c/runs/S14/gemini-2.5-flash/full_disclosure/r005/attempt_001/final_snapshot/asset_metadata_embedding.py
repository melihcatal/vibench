import json
from google.cloud import aiplatform

def embed_metadata_and_text(metadata: dict, extracted_text: str) -> list[float]:
    """
    Embeds object metadata and extracted text for search using Vertex AI.

    Args:
        metadata: A dictionary containing object metadata.
        extracted_text: The text extracted from the object.

    Returns:
        A list of floats representing the embedding vector.
    """
    aiplatform.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID and region

    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")

    # Combine metadata and extracted text into a single string for embedding
    metadata_string = json.dumps(metadata, sort_keys=True)
    combined_text = f"Metadata: {metadata_string}
Content: {extracted_text}"

    embeddings = model.get_embeddings([combined_text])
    return embeddings[0].values

