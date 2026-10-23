from google.cloud import documentai
from document_client import get_documentai_client, build_process_document_request
from document_models import normalize_document_fields

def validate_document_fields(fields: dict) -> bool:
    required_fields = ["merchant", "tax", "total", "items"]
    for field in required_fields:
        if field not in fields:
            return False
    return True