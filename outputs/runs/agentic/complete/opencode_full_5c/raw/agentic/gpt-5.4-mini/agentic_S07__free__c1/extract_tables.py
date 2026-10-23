from document_client import create_client, load_config, process_bytes
from document_models import TableExtractionRequest, tables_from_document


def extract_tables(request: TableExtractionRequest):
    config = load_config()
    client = create_client()
    content = open(request.image_path, "rb").read()
    document = process_bytes(client, config, content, request.mime_type)
    return {"tables": tables_from_document(document)}
