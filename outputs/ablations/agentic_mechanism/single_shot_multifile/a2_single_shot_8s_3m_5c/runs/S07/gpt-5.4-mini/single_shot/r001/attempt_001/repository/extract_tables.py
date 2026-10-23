from google.cloud import documentai
from document_client import get_document_ai_client, get_document_ai_processor_name
from document_models import DocumentTableRequest, TableCell, TableRow, TableResponse, bbox_to_dict


def extract_tables(request: DocumentTableRequest) -> TableResponse:
    client = get_document_ai_client()
    name = get_document_ai_processor_name(request.processor_id, request.location, request.project_id)
    raw_document = documentai.RawDocument(content=request.image_bytes, mime_type=request.mime_type)
    doc = client.process_document(name=name, raw_document=raw_document)
    rows = []
    for page in doc.document.pages:
        for table in page.tables:
            for row in table.body_rows:
                cells = []
                for cell in row.cells:
                    cells.append(TableCell(text=cell.layout.text_anchor.content if cell.layout.text_anchor else "", bbox=bbox_to_dict(cell.layout.bounding_poly)))
                rows.append(TableRow(cells=cells))
    return TableResponse(rows=rows, raw=doc)
