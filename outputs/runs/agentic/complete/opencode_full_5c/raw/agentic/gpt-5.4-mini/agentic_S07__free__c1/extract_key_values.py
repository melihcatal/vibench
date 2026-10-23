from document_client import create_client, load_config, process_bytes
from document_models import KeyValueExtractionRequest, key_values_from_document


def extract_key_values(request: KeyValueExtractionRequest):
    config = load_config()
    client = create_client()
    content = open(request.image_path, "rb").read()
    document = process_bytes(client, config, content, request.mime_type)
    return {"key_values": key_values_from_document(document)}
