import os
from typing import List
from speech_models import TranscriptionResult
from vertexai.language_models import TextEmbeddingModel
import vertexai

def transcript_embedding(transcript_result: TranscriptionResult) -> List[List[float]]:
    """Embed transcript segments for semantic retrieval using Google Cloud Generative AI (Vertex AI).

    Args:
        transcript_result: The TranscriptionResult object containing the transcript segments to embed.

    Returns:
        A list of lists of floats, where each inner list is the embedding for a transcript segment.
    """
    # Initialize Vertex AI
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")  # Replace with your GCP project ID
    location = os.environ.get("GCP_REGION", "us-central1") # Replace with your GCP region
    vertexai.init(project=project_id, location=location)

    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003") # Using textembedding-gecko@003 model

    segments_to_embed = [alt.transcript for alt in transcript_result.alternatives if alt.transcript]

    if not segments_to_embed:
        return []
    
    embeddings = model.get_embeddings(segments_to_embed)

    return [embedding.values for embedding in embeddings]
