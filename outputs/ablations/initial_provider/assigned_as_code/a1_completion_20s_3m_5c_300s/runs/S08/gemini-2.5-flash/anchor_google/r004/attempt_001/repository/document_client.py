import os
from document_models import DocumentConfig

def load_document_config() -> DocumentConfig:
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us")
    document_ai_processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID")
    gemini_model_id = os.environ.get("GEMINI_MODEL_ID", "gemini-pro")
    firestore_collection_id = os.environ.get("FIRESTORE_COLLECTION_ID", "expense_records")

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")
    if not document_ai_processor_id:
        raise ValueError("DOCUMENT_AI_PROCESSOR_ID environment variable not set.")

    return DocumentConfig(
        project_id=project_id,
        location=location,
        processor_id=document_ai_processor_id,
        model_id=gemini_model_id,
        collection_id=firestore_collection_id
    )
