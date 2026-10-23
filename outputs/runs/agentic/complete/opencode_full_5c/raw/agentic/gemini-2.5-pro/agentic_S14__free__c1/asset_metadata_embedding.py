import vertexai
from vertexai.language_models import TextEmbeddingModel
from storage_models import EmbeddingResponse, ObjectMetadata


def asset_metadata_embedding(
    project_id: str,
    location: str,
    metadata: ObjectMetadata,
    extracted_text: str,
    model_name: str = "textembedding-gecko@003",
) -> EmbeddingResponse:
    """
    Generates a text embedding for asset metadata and extracted text.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region.
        metadata: The ObjectMetadata of the asset.
        extracted_text: Text extracted from the asset (e.g., via OCR).
        model_name: The name of the text embedding model.

    Returns:
        An EmbeddingResponse containing the embedding vector.
    """
    vertexai.init(project=project_id, location=location)

    combined_text = (
        f"Object Name: {metadata.name}\n"
        f"Content Type: {metadata.content_type}\n"
        f"Content: {extracted_text}"
    )

    model = TextEmbeddingModel.from_pretrained(model_name)

    embeddings = model.get_embeddings([combined_text])

    embedding_vector = embeddings[0].values

    print(f"Generated embedding for: {metadata.name}")
    print(f"Vector dimension: {len(embedding_vector)}")

    return EmbeddingResponse(embedding=embedding_vector)
