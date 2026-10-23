from google.cloud import aiplatform

from document_models import OCRRequest
from extract_text import extract_text


def ocr_embedding(request: OCRRequest) -> dict:
    source = extract_text(request)
    client = aiplatform.gapic.PredictionServiceClient()
    endpoint = f"projects/{source.raw.get('project', '')}/locations/us-central1/publishers/google/models/textembedding-gecko@003"
    return {"provider": "vertex_ai_textembedding_gecko_003", "text": source.text, "endpoint": endpoint, "client": client.__class__.__name__}
