from google.cloud import documentai_v1 as documentai
from google.cloud import storage
from dataclasses import dataclass
from typing import Optional, Dict
import os


@dataclass
class OCRResponse:
    text: str
    pages: int
    language: str
    confidence: float
    entities: Dict[str, list]


def stored_document_ocr(
    gcs_uri: str, project_id: str, location: str = "us", processor_id: str = None
) -> OCRResponse:
    """
    Runs OCR on a document stored in Google Cloud Storage using Google Document AI.

    Args:
        gcs_uri: GCS URI of the document (e.g., gs://bucket-name/object-name).
        project_id: Google Cloud project ID.
        location: Processor location (e.g., "us").
        processor_id: Document AI processor ID. If None, uses a default OCR processor.

    Returns:
        OCRResponse containing extracted text, page count, language, confidence, and entities.
    """
    if not processor_id:
        processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")
        if not processor_id:
            raise ValueError(
                "Processor ID must be provided or set in GOOGLE_DOCUMENT_AI_PROCESSOR_ID"
            )

    client = documentai.DocumentProcessorServiceClient()
    processor_name = (
        f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    )

    request = {
        "name": processor_name,
        "raw_document": {
            "gcs_uri": gcs_uri,
            "mime_type": "application/pdf",  # Default, can be inferred or passed dynamically
        },
    }

    result = client.process_document(request=request)
    document = result.document

    return OCRResponse(
        text=document.text,
        pages=len(document.pages),
        language=document.language_code,
        confidence=document.confidence,
        entities={
            "entities": [
                {
                    "type": entity.type_,
                    "mention_text": entity.mention_text,
                    "confidence": entity.confidence,
                }
                for entity in document.entities
            ]
        },
    )
