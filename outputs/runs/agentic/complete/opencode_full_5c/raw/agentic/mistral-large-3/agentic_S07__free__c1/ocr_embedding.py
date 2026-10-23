from typing import Dict, List, Optional
import os
from google.cloud import aiplatform
from document_models import OCRResponse


def embed_text(text: str, model_id: str = "textembedding-gecko@latest") -> List[float]:
    """Embed extracted document sections using Google Cloud Vertex AI."""
    client = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"us-central1-aiplatform.googleapis.com"}
    )

    instance = {"content": text}
    instances = [instance]
    endpoint = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/us-central1/publishers/google/models/{model_id}"

    response = client.predict(endpoint=endpoint, instances=instances)
    return response.predictions[0]["embeddings"]["values"]


def ocr_embedding(
    ocr_response: OCRResponse, section_delimiter: str = "\n\n"
) -> Dict[str, List[float]]:
    """Embed extracted document sections for semantic retrieval."""
    sections = ocr_response.text.split(section_delimiter)
    embeddings = {}

    for i, section in enumerate(sections):
        if section.strip():
            embeddings[f"section_{i}"] = embed_text(section)

    return embeddings
