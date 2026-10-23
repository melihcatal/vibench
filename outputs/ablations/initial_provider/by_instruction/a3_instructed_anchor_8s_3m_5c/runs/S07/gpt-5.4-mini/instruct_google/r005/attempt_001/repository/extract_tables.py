from google.cloud import documentai_v1 as documentai

from document_client import documentai_client, documentai_raw_document, get_env, processor_name
from document_models import OCRRequest, TableResponse


def extract_tables(request: OCRRequest) -> TableResponse:
    client = documentai_client()
    name = processor_name(get_env("GOOGLE_CLOUD_PROJECT", ""), get_env("GOOGLE_CLOUD_LOCATION", "us"), get_env("GOOGLE_CLOUD_DOCUMENTAI_TABLE_PROCESSOR_ID", ""))
    raw = documentai_raw_document(request.image_uri, request.image_bytes)
    result = client.process_document(name=name, raw_document=raw)
    document = result.document
    tables = []
    for page in document.pages:
        for table in page.tables:
            tables.append({"header_rows": len(table.header_rows), "body_rows": len(table.body_rows)})
    return TableResponse(tables=tables, raw={"provider": "google_document_ai", "document": document.to_json()})
