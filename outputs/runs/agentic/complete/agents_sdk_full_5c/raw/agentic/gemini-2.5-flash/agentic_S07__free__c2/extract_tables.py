from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import DocumentProcessingRequest, TableExtractionResponse, TableCell, TableRow, ExtractedTable

def extract_tables(request: DocumentProcessingRequest) -> TableExtractionResponse:
    """Extracts table cells and row structure from a document using Google Cloud Document AI.
    The Form Parser processor is often used for this as it can detect and parse tables.
    """
    client = get_documentai_client()

    # FORM_PARSER_PROCESSOR_V1 or TABLE_PARSER_PROCESSOR are suitable.
    # FORM_PARSER_PROCESSOR_V1 is generally capable of table extraction.
    processor_id = "FORM_PARSER_PROCESSOR_V1"  
    name = client.processor_path(request.project_id, request.location, processor_id)

    document = documentai.RawDocument(content=request.file_content, mime_type=request.mime_type)

    response = client.process_document(
        name=name,
        raw_document=document
    )

    extracted_tables = []
    for page in response.document.pages:
        for table in page.tables:
            rows = []
            for document_row in table.body_rows:
                cells = []
                for document_cell in document_row.cells:
                    cell_text = documentai.get_text_anchor_text(document_cell.layout.text_anchor, response.document.text)
                    cells.append(TableCell(content=cell_text))
                rows.append(TableRow(cells=cells))
            
            # Assuming headers are also part of a table structure, though separated in Document AI response
            header_rows = []
            for document_header_row in table.header_rows:
                header_cells = []
                for document_header_cell in document_header_row.cells:
                    header_cell_text = documentai.get_text_anchor_text(document_header_cell.layout.text_anchor, response.document.text)
                    header_cells.append(TableCell(content=header_cell_text))
                header_rows.append(TableRow(cells=header_cells))

            extracted_tables.append(ExtractedTable(header_rows=header_rows, body_rows=rows))

    return TableExtractionResponse(tables=extracted_tables)
