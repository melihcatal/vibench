import os

def get_documentai_config() -> dict:
    """
    Returns configuration for Google Document AI.
    """
    return {
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        "location": os.getenv("GOOGLE_CLOUD_LOCATION", "us"),
        "invoice_processor_id": os.getenv("GOOGLE_DOCUMENTAI_INVOICE_PROCESSOR_ID"),
    }

def get_mindee_config() -> dict:
    """
    Returns configuration for Mindee.
    """
    return {
        "api_key": os.getenv("MINDEE_API_KEY"),
    }

def get_gemini_config() -> dict:
    """
    Returns configuration for Google Gemini API.
    """
    return {
        "api_key": os.getenv("GOOGLE_API_KEY"),
        "model_name": os.getenv("GEMINI_MODEL_NAME", "gemini-pro"),
    }

def get_azure_content_safety_config() -> dict:
    """
    Returns configuration for Azure AI Content Safety.
    """
    return {
        "endpoint": os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
        "key": os.getenv("AZURE_CONTENT_SAFETY_KEY"),
    }

def get_google_translate_config() -> dict:
    """
    Returns configuration for Google Cloud Translation.
    """
    return {
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
    }

def get_firestore_config() -> dict:
    """
    Returns configuration for Google Firestore.
    """
    return {
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        "collection_name": os.getenv("FIRESTORE_COLLECTION_NAME", "expense_records"),
    }
