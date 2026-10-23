from google.cloud import documentai_v1 as documentai
import os

def extract_tables_from_document(project_id: str, location: str, processor_id: str, file_path: str):
    """Extracts tables from a document using Google Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    extracted_tables = []
    for page in document.pages:
        for table in page.tables:
            table_data = {
                "num_rows": table.num_rows,
                "num_columns": table.num_columns,
                "header_rows": [],
                "body_rows": []
            }
            for row in table.header_rows:
                header_cells = []
                for cell in row.cells:
                    header_cells.append(document.text[cell.layout.text_anchor.text_segments[0].start_index:cell.layout.text_anchor.text_segments[0].end_index])
                table_data["header_rows"].append(header_cells)
            for row in table.body_rows:
                body_cells = []
                for cell in row.cells:
                    body_cells.append(document.text[cell.layout.text_anchor.text_segments[0].start_index:cell.layout.text_anchor.text_segments[0].end_index])
                table_data["body_rows"].append(body_cells)
            extracted_tables.append(table_data)
    
    return extracted_tables

if __name__ == '__main__':
    # Placeholder values for demonstration
    PROJECT_ID = "your-gcp-project-id"
    LOCATION = "us"
    PROCESSOR_ID = "your-form-parser-processor-id" # Use a Form Parser or Table Parser processor
    FILE_PATH = "path/to/your/document.pdf"

    # tables = extract_tables_from_document(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)
    # for i, table in enumerate(tables):
    #     print(f"Table {i+1}:")
    #     print(f"  Header: {table['header_rows']}")
    #     print(f"  Body: {table['body_rows']}")
