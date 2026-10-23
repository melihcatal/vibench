from document_client import get_documentai_client, get_processor_path
from document_models import DocumentRequest, TableExtractionResponse, Table, TableRow, TableCell
from google.cloud.documentai_v1.types import RawDocument

def extract_tables_from_document(
    document_request: DocumentRequest,
    project_id: str,
    location: str,
    processor_id: str,
) -> TableExtractionResponse:
    """
    Extracts table cells and row structure from a document using Google Document AI.
    """
    client = get_documentai_client()
    processor_path = get_processor_path(project_id, location, processor_id)

    raw_document = RawDocument(content=document_request.content, mime_type=document_request.mime_type)
    
    request = {"name": processor_path, "raw_document": raw_document}
    result = client.process_document(request=request)
    
    document = result.document

    extracted_tables = []
    for page in document.pages:
        for table_proto in page.tables:
            rows = []
            for row_proto in table_proto.header_rows + table_proto.body_rows:
                cells = []
                for cell_proto in row_proto.cells:
                    cell_text = document.text[cell_proto.layout.text_anchor.text_segments[0].start_index:cell_proto.layout.text_anchor.text_segments[0].end_index]
                    cells.append(TableCell(content=cell_text.strip()))
                rows.append(TableRow(cells=cells))
            extracted_tables.append(Table(rows=rows))
            
    return TableExtractionResponse(text_content=document.text, tables=extracted_tables)

