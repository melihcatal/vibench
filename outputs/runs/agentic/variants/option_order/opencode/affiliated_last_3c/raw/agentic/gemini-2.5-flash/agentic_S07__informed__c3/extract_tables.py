from google.cloud import documentai_v1 as documentai
import os


def extract_tables(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts table cells and row structure from a document using Google Document AI.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )  # Assuming PDF

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)

    document_tables = []
    for page in result.document.pages:
        for table in page.tables:
            table_data = {"body_rows": [], "header_rows": []}
            for row in table.header_rows:
                header_cells = []
                for cell in row.cells:
                    header_cells.append(
                        cell.layout.text_anchor.text_segments[0].text_content
                        if cell.layout.text_anchor.text_segments
                        else ""
                    )
                table_data["header_rows"].append(header_cells)
            for row in table.body_rows:
                body_cells = []
                for cell in row.cells:
                    body_cells.append(
                        cell.layout.text_anchor.text_segments[0].text_content
                        if cell.layout.text_anchor.text_segments
                        else ""
                    )
                table_data["body_rows"].append(body_cells)
            document_tables.append(table_data)

    return document_tables


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"  # e.g., "us"
    processor_id = os.environ.get(
        "GOOGLE_DOCUMENT_AI_PROCESSOR_ID"
    )  # e.g., "YOUR_PROCESSOR_ID"
    file_path = "path/to/your/document.pdf"  # Replace with your document path
    # tables = extract_tables(project_id, location, processor_id, file_path)
    # import json
    # print(json.dumps(tables, indent=2))
