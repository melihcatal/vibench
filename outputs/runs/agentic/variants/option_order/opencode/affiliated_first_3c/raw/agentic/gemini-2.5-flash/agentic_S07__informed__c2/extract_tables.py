from google.cloud import documentai_v1beta3 as documentai
from document_client import get_documentai_client
from document_models import DocumentRequest, TableExtractionResponse, Table


def extract_tables(request: DocumentRequest) -> TableExtractionResponse:
    client = get_documentai_client()
    processor_name = client.processor_path(
        request.project_id, request.location, request.processor_id
    )

    raw_document = documentai.RawDocument(
        content=request.file_content,
        mime_type=request.mime_type,
    )
    request_options = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )

    result = client.process_document(request=request_options)

    tables = []
    for page in result.document.pages:
        for table_proto in page.tables:
            current_table = Table(rows=[])
            for row_proto in table_proto.body_rows:
                row_cells = []
                for cell_proto in row_proto.cells:
                    row_cells.append(
                        client.get_text(
                            result.document.text, cell_proto.layout.text_anchor
                        )
                    )
                current_table.rows.append(row_cells)
            tables.append(current_table)

    return TableExtractionResponse(tables=tables)
