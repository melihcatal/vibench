
from google.cloud import aiplatform

def embed_text_with_vertex_ai(
    project_id: str,
    location: str,
    text_to_embed: str
) -> list[float]:
    """Embeds text using a Vertex AI embedding model.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region where your model is deployed (e.g., "us-central1").
        text_to_embed: The text string to embed.

    Returns:
        A list of floats representing the embedding vector.
    """
    aiplatform.init(project=project_id, location=location)

    # The model ID for the text-embedding-004 model
    # For other models, refer to https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/text-embeddings
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")

    # The maximum number of texts that can be embedded in a single request is 5.
    # For this example, we are embedding a single text string.
    embeddings = model.get_embeddings([text_to_embed])
    return embeddings[0].values

def embed_object_metadata_and_text(
    project_id: str,
    location: str,
    metadata: dict,
    extracted_text: str
) -> list[float]:
    """Combines object metadata and extracted text, then embeds them for search.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region where your model is deployed.
        metadata: A dictionary of object metadata (e.g., {"filename": "doc.pdf", "author": "John Doe"}).
        extracted_text: The text extracted from the object.

    Returns:
        A list of floats representing the combined embedding vector.
    """
    # Combine metadata and extracted text into a single string for embedding
    metadata_string = " ".join([f"{k}: {v}" for k, v in metadata.items()])
    combined_text = f"Metadata: {metadata_string}. Content: {extracted_text}"

    return embed_text_with_vertex_ai(project_id, location, combined_text)
