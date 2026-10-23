import os

def get_google_documentai_credentials() -> dict:
    """
    Returns Google Document AI credentials from environment variables.
    """
    return {
        "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT_ID"),
        "location": os.environ.get("GOOGLE_CLOUD_LOCATION"),
        "invoice_processor_id": os.environ.get("GOOGLE_CLOUD_INVOICE_PROCESSOR_ID"),
    }

def get_azure_formrecognizer_credentials() -> dict:
    """
    Returns Azure Form Recognizer credentials from environment variables.
    """
    return {
        "endpoint": os.environ.get("AZURE_FORM_RECOGNIZER_ENDPOINT"),
        "key": os.environ.get("AZURE_FORM_RECOGNIZER_KEY"),
    }

def get_openai_credentials() -> dict:
    """
    Returns OpenAI API key from environment variables.
    """
    return {
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }

def get_google_nlp_credentials() -> dict:
    """
    Returns Google Cloud Natural Language API credentials from environment variables.
    """
    return {
        "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT_ID"),
    }

def get_google_translate_credentials() -> dict:
    """
    Returns Google Cloud Translation API credentials from environment variables.
    """
    return {
        "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT_ID"),
    }

def get_mongodb_atlas_credentials() -> dict:
    """
    Returns MongoDB Atlas credentials from environment variables.
    """
    return {
        "connection_string": os.environ.get("MONGODB_ATLAS_CONNECTION_STRING"),
        "database_name": os.environ.get("MONGODB_ATLAS_DATABASE_NAME"),
        "collection_name": os.environ.get("MONGODB_ATLAS_COLLECTION_NAME"),
    }
