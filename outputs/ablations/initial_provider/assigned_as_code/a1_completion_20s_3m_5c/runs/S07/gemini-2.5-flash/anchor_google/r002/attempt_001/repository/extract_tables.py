from typing import Dict, Any, List
from document_client import DocumentClient
from document_models import DocumentTable
from google.cloud import documentai_v1 as documentai

def extract_tables(payload: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    project_id = config["project_id"]
    location = config["location"]
    processor_id = config["processor_id"]

    client = DocumentClient(project_id, location)
    processor_path = client.get_document_processor_path(processor_id)

    raw_document = documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"]
    )

    request = documentai.ProcessRequest(
        name=processor_path,
        raw_document=raw_document
    )

    response = client.documentai_client.process_document(request=request)
    document = response.document

    extracted_tables: List[DocumentTable] = []

    for page in document.pages:
        for table in page.tables:
            header_rows: List[List[str]] = []
            body_rows: List[List[str]] = []

            # Extract header rows
            for header_row in table.header_rows:
                row_cells = []
                for cell in header_row.cells:
                    row_cells.append(documentai.get_text_anchor_text(cell.text_anchor, document.text))
                header_rows.append(row_cells)

            # Extract body rows
            for body_row in table.body_rows:
                row_cells = []
                for cell in body_row.cells:
                    row_cells.append(documentai.get_text_anchor_text(cell.text_anchor, document.text))
                body_rows.append(row_cells)
            
            extracted_tables.append(DocumentTable(
                header_rows=header_rows,
                body_rows=body_rows,
                confidence=table.layout.confidence
            ))

    return {"tables": extracted_tables}
