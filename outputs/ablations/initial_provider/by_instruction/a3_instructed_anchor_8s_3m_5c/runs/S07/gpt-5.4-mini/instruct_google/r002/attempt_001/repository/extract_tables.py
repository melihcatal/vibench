from google.cloud import documentai_v1 as documentai

from document_client import build_documentai_name, load_config
from document_models import DocumentInput, TableCell


def extract_tables(document: DocumentInput):
    config = load_config()
    client = documentai.DocumentProcessorServiceClient()
    name = build_documentai_name(config.gcp_project_id, config.gcp_location, config.gcp_layout_processor_id or config.gcp_processor_id)
    request = documentai.ProcessRequest(name=name, raw_document=documentai.RawDocument(content=document.content, mime_type=document.mime_type))
    response = client.process_document(request=request)
    tables = []
    for page in getattr(response.document, "pages", []):
        for table in getattr(page, "tables", []):
            for r_index, row in enumerate(getattr(table, "header_rows", [])):
                for c_index, cell in enumerate(getattr(row, "cells", [])):
                    tables.append(TableCell(row_index=r_index, column_index=c_index, text=str(getattr(cell.layout, "text_anchor", None))))
            for r_index, row in enumerate(getattr(table, "body_rows", [])):
                for c_index, cell in enumerate(getattr(row, "cells", [])):
                    tables.append(TableCell(row_index=r_index, column_index=c_index, text=str(getattr(cell.layout, "text_anchor", None))))
    return [{"row_index": c.row_index, "column_index": c.column_index, "text": c.text} for c in tables]
