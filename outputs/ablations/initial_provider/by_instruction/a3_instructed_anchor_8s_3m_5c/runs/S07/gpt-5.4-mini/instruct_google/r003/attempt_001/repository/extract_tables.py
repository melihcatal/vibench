import os

from document_client import process_document


def extract_tables(content: str, mime_type: str = "image/png"):
    result = process_document(content=content, mime_type=mime_type, processor_id=os.environ["GOOGLE_DOCUMENT_AI_TABLE_PROCESSOR_ID"])
    document = result["document"]
    tables = []
    for page in getattr(document, "pages", []):
        for table in getattr(page, "tables", []):
            tables.append({"header_rows": len(getattr(table, "header_rows", [])), "body_rows": len(getattr(table, "body_rows", []))})
    return tables
