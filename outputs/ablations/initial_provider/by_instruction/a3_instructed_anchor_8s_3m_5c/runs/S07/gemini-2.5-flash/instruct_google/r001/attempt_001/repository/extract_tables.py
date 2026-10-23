from document_client import get_document_processor_client
from document_models import ExtractedTable, TableCell
from google.cloud import documentai_v1 as documentai

def extract_tables(project_id: str, location: str, processor_id: str, file_content: bytes, mime_type: str) -> list[ExtractedTable]:
    client = get_document_processor_client()
    
    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    raw_document = documentai.RawDocument(
        content=file_content,
        mime_type=mime_type
    )

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document
    )

    result = client.process_document(request=request)
    document = result.document

    extracted_tables = []
    for page in document.pages:
        for table in page.tables:
            header_rows_data = []
            for header_row in table.header_rows:
                row_cells = []
                for cell in header_row.cells:
                    row_cells.append(TableCell(text_content=cell.layout.text_anchor.content, row_span=cell.row_span, col_span=cell.col_span))
                header_rows_data.append(row_cells)
            
            body_rows_data = []
            for body_row in table.body_rows:
                row_cells = []
                for cell in body_row.cells:
                    row_cells.append(TableCell(text_content=cell.layout.text_anchor.content, row_span=cell.row_span, col_span=cell.col_span))
                body_rows_data.append(row_cells)
            
            extracted_tables.append(ExtractedTable(num_rows=len(table.header_rows) + len(table.body_rows), num_columns=len(table.header_rows[0].cells) if table.header_rows else 0, header_rows=header_rows_data, body_rows=body_rows_data))
    
    return extracted_tables
