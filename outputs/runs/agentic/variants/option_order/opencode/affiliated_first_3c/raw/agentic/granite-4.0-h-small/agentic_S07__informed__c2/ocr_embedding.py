import os
import json
from document_client import OcrClient
from document_models import OCRResponse
from ibm_watsonx_ai import WatsonxApi, EmbeddingsModel


def compute_ocr_embeddings(image_path: str) -> List[Dict[str, float]]:
    """Embed extracted document sections for semantic retrieval.

    Uses watsonx.ai text embeddings API. Embed each paragraph extracted from the document.
    Prerequisites: set environment variables WATSONX_API_KEY, WATSONX_PROJECT_ID, PROVIDER="google" or "azure" for OCR.
    """
    client = OcrClient()
    ocr_result: OCRResponse = client.process_document(open(image_path, "rb").read())
    text = ocr_result["text"]
    # Split into paragraphs (very naive split on double newlines)
    paragraphs = [p for p in text.split("\n\n") if p.strip()]

    # Watsonx embeddings client
    embeddings = WatsonxApi(
        api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
    )
    model = EmbeddingsModel(
        "google-geo-embed-v1"
    )  # example model ID for IBM Slate embeds
    embeddings_response = embeddings.create_embeddings(
        input_documents=paragraphs, model=model
    )

    # Return list of embeddings as dict with paragraph text and embedding vector
    return [
        {"paragraph": p, "embedding": vec.tolist()}
        for p, vec in zip(paragraphs, embeddings_response.embeddings)
    ]
