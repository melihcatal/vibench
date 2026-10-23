import os
from google.cloud import documentai_v1 as documentai

def extract_tables(project_id: str, location: str, processor_id: str, file_content: bytes, mime_type: str) -> list[dict]:
    """Extracts table cells and row structure from a document using Google Cloud Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    processor_name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    extracted_tables = []
    for page in document.pages:
        for table in page.tables:
            table_data = {
                "num_rows": table.num_rows,
                "num_cols": table.num_cols,
                "header_rows": [],
                "body_rows": []
            }

            for row in table.header_rows:
                header_cells = []
                for cell in row.cells:
                    # Extract text using the text_anchor
                    cell_text = ""
                    for segment in cell.layout.text_anchor.text_segments:
                        start = int(segment.start_index)
                        end = int(segment.end_index)
                        cell_text += document.text[start:end]
                    header_cells.append({
                        "text": cell_text,
                        "row_span": cell.row_span,
                        "col_span": cell.col_span
                    })
                table_data["header_rows"].append(header_cells)

            for row in table.body_rows:
                body_cells = []
                for cell in row.cells:
                    cell_text = ""
                    for segment in cell.layout.text_anchor.text_segments:
                        start = int(segment.start_index)
                        end = int(segment.end_index)
                        cell_text += document.text[start:end]
                    body_cells.append({
                        "text": cell_text,
                        "row_span": cell.row_span,
                        "col_span": cell.col_span
                    })
                table_data["body_rows"].append(body_cells)
            extracted_tables.append(table_data)

    return extracted_tables

if __name__ == '__main__':
    # Example usage (replace with your actual project, location, processor, and file)
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # location = "us"  # e.g., "us" or "eu"
    # processor_id = "YOUR_PROCESSOR_ID" # e.g., a "Form Parser" or "Table Parser" processor
    #
    # if project_id and processor_id:
    #     with open("path/to/your/document_with_tables.pdf", "rb") as doc_file:
    #         content = doc_file.read()
    #         mime_type = "application/pdf"
    #         tables_info = extract_tables(project_id, location, processor_id, content, mime_type)
    #         for i, table in enumerate(tables_info):
    #             print(f"Table {i+1}:")
    #             print(f"  Rows: {table['num_rows']}, Cols: {table['num_cols']}")
    #             print("  Headers:", table["header_rows"])
    #             print("  Body:", table["body_rows"])
    # else:
    #     print("Please set GOOGLE_CLOUD_PROJECT and provide a processor_id.")
    pass
