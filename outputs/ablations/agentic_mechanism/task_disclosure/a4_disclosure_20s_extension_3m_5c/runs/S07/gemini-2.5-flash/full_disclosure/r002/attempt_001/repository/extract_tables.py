from google.cloud import documentai_v1 as documentai
import io

def _get_text_from_text_anchor(text_anchor: documentai.Document.TextAnchor, text_content: str) -> str:
    if not text_anchor.text_segments:
        return ""
    segments = []
    for segment in text_anchor.text_segments:
        start_index = int(segment.start_index) if segment.start_index is not None else 0
        end_index = int(segment.end_index) if segment.end_index is not None else len(text_content)
        segments.append(text_content[start_index:end_index])
    return "".join(segments)

def extract_tables_from_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
) -> dict:
    client = documentai.DocumentProcessorServiceClient()
    resource_name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type=mime_type
    )

    request = documentai.ProcessRequest(
        name=resource_name,
        raw_document=raw_document,
    )

    result = client.process_document(request=request)
    document = result.document

    extracted_tables = []
    if document.pages:
        for page in document.pages:
            if page.tables:
                for table_index, table in enumerate(page.tables):
                    table_data = {
                        "page_number": page.page_number,
                        "table_index": table_index,
                        "header_rows": [],
                        "body_rows": [],
                    }

                    for header_row in table.header_rows:
                        row_cells = []
                        for cell in header_row.cells:
                            cell_text = _get_text_from_text_anchor(cell.layout.text_anchor, document.text)
                            row_cells.append(cell_text)
                        table_data["header_rows"].append(row_cells)

                    for body_row in table.body_rows:
                        row_cells = []
                        for cell in body_row.cells:
                            cell_text = _get_text_from_text_anchor(cell.layout.text_anchor, document.text)
                            row_cells.append(cell_text)
                        table_data["body_rows"].append(row_cells)
                    extracted_tables.append(table_data)

    return {"tables": extracted_tables, "text_content": document.text}