from google.cloud import aiplatform
from speech_models import TranscriptionResult
import numpy as np
import os


def transcript_embedding(transcript: TranscriptionResult) -> dict:
    aiplatform.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )

    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@003")

    embeddings = {}
    for segment in transcript.segments:
        response = model.get_embeddings([segment.text])
        embedding = response[0].values
        embeddings[segment.text] = np.array(embedding).tolist()

    return embeddings
