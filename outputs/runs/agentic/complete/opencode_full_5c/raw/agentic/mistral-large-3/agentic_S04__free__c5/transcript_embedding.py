from google.cloud import aiplatform
from speech_models import TranscriptionResult
import os


def transcript_embedding(transcript: TranscriptionResult) -> list:
    """Embed transcript segments for semantic retrieval using Google Cloud Vertex AI."""
    aiplatform.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_REGION"),
    )

    texts = [segment.text for segment in transcript.segments]
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@latest")
    embeddings = model.get_embeddings(texts)

    return [embedding.values for embedding in embeddings]
