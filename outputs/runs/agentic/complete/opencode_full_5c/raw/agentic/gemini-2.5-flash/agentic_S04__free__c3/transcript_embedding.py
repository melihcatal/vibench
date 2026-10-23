import vertexai
from vertexai.language_models import TextEmbeddingModel
from speech_models import EmbeddingRequest


def embed_transcript_segments(request: EmbeddingRequest) -> list[list[float]]:
    """Embeds transcript segments for semantic retrieval using Google Cloud Generative AI embedding model."""
    # TODO: Replace with your Google Cloud Project ID and region
    vertexai.init(project="your-google-cloud-project-id", location="us-central1")

    model = TextEmbeddingModel.from_pretrained(
        "text-embedding-004"
    )  # Or other embedding models

    embeddings = model.get_embeddings(request.text_segments)

    return [embedding.values for embedding in embeddings]
