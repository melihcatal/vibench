from google.cloud import documentai_v1b3 as documentai
import os


def extract_layout(project_id: str, location: str, processor_id: str, file_path: str):
    """Extracts layout elements (pages, blocks, paragraphs, lines, tokens, etc.) from a document using Google Document AI."""
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    layout_info = []
    for page in document.pages:
        page_layout = {
            "page_number": page.page_number,
            "blocks": [],
            "paragraphs": [],
            "lines": [],
            "tokens": [],
        }
        for block in page.blocks:
            page_layout["blocks"].append(documentai.Document.to_json(block))
        for paragraph in page.paragraphs:
            page_layout["paragraphs"].append(documentai.Document.to_json(paragraph))
        for line in page.lines:
            page_layout["lines"].append(documentai.Document.to_json(line))
        for token in page.tokens:
            page_layout["tokens"].append(documentai.Document.to_json(token))
        layout_info.append(page_layout)
    return layout_info


if __name__ == "__main__":
    # Example usage (replace with your actual values)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    LOCATION = "us"  # e.g., "us"
    PROCESSOR_ID = "YOUR_PROCESSOR_ID"  # Create a "OCR_PROCESSOR" in Document AI
    FILE_PATH = "path/to/your/document.pdf"

    if PROJECT_ID and PROCESSOR_ID and os.path.exists(FILE_PATH):
        extracted_layout = extract_layout(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)
        print("Extracted Layout:\n", extracted_layout)
    else:
        print(
            "Please set GOOGLE_CLOUD_PROJECT, PROCESSOR_ID, and provide a valid FILE_PATH."
        )
