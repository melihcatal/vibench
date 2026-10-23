from google.cloud import documentai_v1beta3 as documentai
import os
from document_client import get_documentai_client


def extract_tables_from_document(
    project_id: str, location: str, processor_id: str, file_path: str
):
    """
    Extracts table cells and row structure from a document using Google Document AI.
    """
    client = get_documentai_client()

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    tables_info = []
    for page in document.pages:
        for table in page.tables:
            table_data = []
            header_row = (
                [
                    page.get_text(cell.layout.text_anchor)
                    for cell in table.header_rows[0].cells
                ]
                if table.header_rows
                else []
            )
            if header_row:  # Add header if exists
                table_data.append(header_row)
            for row in table.body_rows:
                row_data = [
                    page.get_text(cell.layout.text_anchor) for cell in row.cells
                ]
                table_data.append(row_data)
            tables_info.append(
                {"page_number": page.page_number, "table_data": table_data}
            )

    return tables_info
