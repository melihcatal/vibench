import os
from typing import Any, Dict

def load_config(service_name: str) -> Dict[str, Any]:
    """
    Loads configuration for a given service from environment variables.
    This is a placeholder for a more robust configuration management system.
    """
    config = {}
    if service_name == "documentai":
        config["project_id"] = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        config["location"] = os.environ.get("DOCUMENT_AI_LOCATION", "us")
        config["invoice_processor_id"] = os.environ.get("DOCUMENT_AI_INVOICE_PROCESSOR_ID")
    elif service_name == "textract":
        config["region_name"] = os.environ.get("AWS_REGION", "us-east-1")
    elif service_name == "gemini":
        config["api_key"] = os.environ.get("GEMINI_API_KEY")
        config["model_name"] = os.environ.get("GEMINI_MODEL_NAME", "gemini-pro")
    elif service_name == "rekognition":
        config["region_name"] = os.environ.get("AWS_REGION", "us-east-1")
    elif service_name == "translation":
        config["project_id"] = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        config["location"] = os.environ.get("TRANSLATE_LOCATION", "global")
    elif service_name == "mongodb":
        config["connection_string"] = os.environ.get("MONGODB_CONNECTION_STRING")
        config["database_name"] = os.environ.get("MONGODB_DATABASE_NAME", "expense_db")
        config["collection_name"] = os.environ.get("MONGODB_COLLECTION_NAME", "expense_records")
    
    return config

def get_document_path_from_env() -> str:
    """
    Retrieves a document path from an environment variable for examples.
    """
    return os.environ.get("DOCUMENT_PATH", "")


if __name__ == '__main__':
    # Example Usage
    doc_ai_config = load_config("documentai")
    print("Document AI Config:", doc_ai_config)

    textract_config = load_config("textract")
    print("Textract Config:", textract_config)

    gemini_config = load_config("gemini")
    print("Gemini Config:", gemini_config)

    doc_path = get_document_path_from_env()
    print("Document Path from ENV:", doc_path)
