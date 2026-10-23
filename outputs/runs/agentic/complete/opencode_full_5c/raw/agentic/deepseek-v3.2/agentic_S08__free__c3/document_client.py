import os
from google.cloud import documentai
from google.api_core.client_options import ClientOptions


def get_documentai_client():
    location = os.environ.get("DOCUMENTAI_LOCATION", "us")

    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    return client


def load_config():
    config = {
        "google_cloud_project": os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project"),
        "documentai_location": os.environ.get("DOCUMENTAI_LOCATION", "us"),
        "documentai_invoice_processor_id": os.environ.get(
            "DOCUMENTAI_INVOICE_PROCESSOR_ID", "invoice-processor"
        ),
        "documentai_receipt_processor_id": os.environ.get(
            "DOCUMENTAI_RECEIPT_PROCESSOR_ID", "receipt-processor"
        ),
        "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
        "openai_model": os.environ.get("OPENAI_MODEL", "gpt-4"),
        "mongodb_uri": os.environ.get("MONGODB_URI", "mongodb://localhost:27017"),
        "mongodb_database": os.environ.get("MONGODB_DATABASE", "expenses"),
        "mongodb_collection": os.environ.get("MONGODB_COLLECTION", "expense_records"),
    }
    return config


def parse_documentai_response(document):
    entities = []
    for entity in document.entities:
        entity_data = {
            "type": entity.type_,
            "text": entity.mention_text,
            "confidence": entity.confidence,
            "normalized_value": entity.normalized_value.text
            if entity.normalized_value
            else None,
        }
        entities.append(entity_data)

    return {
        "text": document.text,
        "entities": entities,
        "pages": len(document.pages) if document.pages else 0,
    }
