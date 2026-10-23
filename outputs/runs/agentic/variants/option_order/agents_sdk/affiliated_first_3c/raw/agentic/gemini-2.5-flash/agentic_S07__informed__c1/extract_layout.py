import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client, get_processor_path

def extract_layout_elements(project_id: str, location: str, processor_id: str, file_path: str):
    """Extracts layout elements (blocks, paragraphs, lines) from a document using Google Document AI."""
    client = get_documentai_client()
    processor_path = get_processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    document = documentai.RawDocument(content=image_content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=processor_path, raw_document=document)

    response = client.process_document(request=request)
    doc = response.document

    layout_elements = {
        "text": doc.text,
        "pages": []
    }

    for page in doc.pages:
        page_elements = {
            "page_number": page.page_number,
            "paragraphs": [],
            "lines": []
        }
        for paragraph in page.paragraphs:
            page_elements["paragraphs"].append(doc.text[paragraph.layout.text_anchor.text_segments[0].start_index:paragraph.layout.text_anchor.text_segments[0].end_index])
        for line in page.lines:
            page_elements["lines"].append(doc.text[line.layout.text_anchor.text_segments[0].start_index:line.layout.text_anchor.text_segments[0].end_index])
        layout_elements["pages"].append(page_elements)

    return layout_elements

if __name__ == '__main__':
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    LOCATION = "us"
    PROCESSOR_ID = os.getenv("DOCUMENTAI_PROCESSOR_ID", "your-general-processor-id") # e.g., "ocr-v1"
    SAMPLE_FILE = "path/to/your/document.pdf"

    # layout = extract_layout_elements(PROJECT_ID, LOCATION, PROCESSOR_ID, SAMPLE_FILE)
    # print(layout)
