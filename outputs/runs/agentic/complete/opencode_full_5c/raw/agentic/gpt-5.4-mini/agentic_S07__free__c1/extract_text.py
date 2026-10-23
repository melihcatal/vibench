from document_client import create_client, load_config, process_bytes
from document_models import TextExtractionRequest, normalize_text, text_from_document


def extract_text(request: TextExtractionRequest) -> str:
    config = load_config()
    client = create_client()
    content = open(request.image_path, "rb").read()
    document = process_bytes(client, config, content, request.mime_type)
    return normalize_text(text_from_document(document))
