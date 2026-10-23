from google.cloud import aiplatform
from document_client import get_vertex_ai_prediction_client
from document_models import ExtractedText, TextEmbedding
from typing import List

PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID"  # Replace with your project ID
LOCATION = "us-central1"
PUBLISHER = "google"
MODEL_NAME = "text-embedding-garden"


def embed_ocr_sections(texts: List[ExtractedText]) -> List[TextEmbedding]:
    client = get_vertex_ai_prediction_client()

    endpoint = f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/{PUBLISHER}/models/{MODEL_NAME}"

    instances = [
        {
            "content": t.text,
            "task_type": "RETRIEVAL_QUERY",  # Or "SEMANTIC_SIMILARITY", "CLASSIFICATION", etc.
            "title": "",
        }
        for t in texts
    ]

    response = client.predict(
        endpoint=endpoint,
        instances=instances,
    )

    embeddings = []
    for prediction in response.predictions:
        # Assuming the embedding is directly in the 'embedding' key
        embeddings.append(TextEmbedding(embedding=prediction["embeddings"]["values"]))

    return embeddings
