# extract_text.py
import os
from typing import Any

# Local helpers
from document_client import document_client
from document_models import OCRRequest, OCRResult

# Google Document AI constants (processor ID for General Document OCR)
DOC_AI_ENDPOINT = os.getenv('GOOGLE_DOCUMENTAI_ENDPOINT', 'https://documentai.googleapis.com/v1/projects/{project_id}/locations/us-central1/processors/{processor_id}')