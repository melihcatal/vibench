from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import DocumentPayload, DocumentConfig, TableExtractionResult


def extract_tables(payload: DocumentPayload, config: DocumentConfig) -> TableExtractionResult:
    client = get_documentai_client(config.location)
    name = client.processor_path(config.project_id, config.location, config.processor_id)
    
    raw_document = documentai.RawDocument(
        content=payload.document_bytes, mime_type=payload.mime_type
    )
    
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    response = client.process_document(request=request)
    
    document = response.document
    
    tables_data = []
    for page in document.pages:
        for table in page.tables:
            header_rows = []
            for row in table.header_rows:
                cells = []
                for cell in row.cells:
                    cells.append({
                        "text": client.common.text_anchor_to_string(cell.layout.text_anchor, document.text),
                        "row_span": cell.row_span,
                        "col_span": cell.col_span,
                    })
                header_rows.append({"cells": cells})

            body_rows = []
            for row in table.body_rows:
                cells = []
                for cell in row.cells:
                    cells.append({
                        "text": client.common.text_anchor_to_string(cell.layout.text_anchor, document.text),
                        "row_span": cell.row_span,
                        "col_span": cell.col_span,
                    })
                body_rows.append({"cells": cells})

            tables_data.append({
                "page_number": page.page_number,
                "header_rows": header_rows,
                "body_rows": body_rows,
                "text": client.common.text_anchor_to_string(table.layout.text_anchor, document.text)
            })

    return TableExtractionResult(tables=tables_data)
