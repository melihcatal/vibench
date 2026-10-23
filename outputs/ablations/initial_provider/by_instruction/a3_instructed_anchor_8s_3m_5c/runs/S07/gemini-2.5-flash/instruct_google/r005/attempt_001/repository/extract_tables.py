from google.cloud import documentai_v1 as documentai
from typing import List, Dict, Any
from document_models import DocumentInput, ExtractedTable

def extract_tables_from_document(document_input: DocumentInput, project_id: str, location: str, processor_id: str) -> ExtractedTable:
    """Extracts table cells and row structure from a document using Google Cloud Document AI.

    This function assumes a Document AI processor specialized for table extraction is used.
    """
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    # e.g., projects/project_id/locations/location/processors/processor_id
    processor_name = client.processor_path(project_id, location, processor_id)

    with open(document_input.image_path, "rb") as image_file:
        image_content = image_file.read()

    # Configure the process request
    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type=document_input.mime_type
    )
    
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    extracted_tables_data = []
    for page in document.pages:
        for table_idx, table in enumerate(page.tables):
            table_data = {
                "page_number": page.page_number,
                "bounding_box": [ (v.x, v.y) for v in table.layout.bounding_poly.vertices ],
                "header_rows": [],
                "body_rows": []
            }

            for row_type, rows in [("header_rows", table.header_rows), ("body_rows", table.body_rows)]:
                for row in rows:
                    cells_data = []
                    for cell in row.cells:
                        cell_text = documentai.Document.to_markdown(cell.layout.text_anchor, document.text)
                        cells_data.append({
                            "text_content": cell_text,
                            "bounding_box": [ (v.x, v.y) for v in cell.layout.bounding_poly.vertices ],
                            "row_span": cell.row_span,
                            "col_span": cell.col_span,
                        })
                    table_data[row_type].append(cells_data)
            extracted_tables_data.append(table_data)
            
    return ExtractedTable(table_data=extracted_tables_data)

if __name__ == "__main__":
    # Example usage: Replace with your project_id, location, processor_id and a valid image path
    # PROJECT_ID = "your-gcp-project-id"
    # LOCATION = "us"
    # PROCESSOR_ID = "your-document-ai-table-processor-id"
    # document_input = DocumentInput(image_path="path/to/your/table_document.png", mime_type="image/png")
    # extracted_tables = extract_tables_from_document(document_input, PROJECT_ID, LOCATION, PROCESSOR_ID)
    # print(extracted_tables.table_data)
    pass
