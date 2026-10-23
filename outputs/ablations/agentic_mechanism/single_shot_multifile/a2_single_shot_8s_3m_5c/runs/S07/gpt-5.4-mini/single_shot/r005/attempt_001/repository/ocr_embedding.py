import os
from typing import List

from google.cloud import aiplatform

from document_models import EmbeddingResponse, OCRResponse


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", os.getenv("GCP_PROJECT", ""))
REGION = os.getenv("VERTEX_AI_REGION", "us-central1")
EMBED_MODEL_ID = os.getenv("VERTEX_EMBED_MODEL_ID", "textembedding-gecko@003")


def embed_ocr_sections(ocr: OCRResponse) -> EmbeddingResponse:
    aiplatform.init(project=PROJECT_ID, location=REGION)
    model = aiplatform.TextEmbeddingModel.from_pretrained(EMBED_MODEL_ID)
    sections: List[str] = [s for s in ocr.text.split("\n\n") if s.strip()]
    embeddings = model.get_embeddings(sections)
    vectors = [emb.values for emb in embeddings]
    return EmbeddingResponse(embeddings=vectors, raw=embeddings)
