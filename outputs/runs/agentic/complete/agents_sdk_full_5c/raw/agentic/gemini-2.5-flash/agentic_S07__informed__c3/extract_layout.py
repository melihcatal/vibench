import os
from google.cloud import documentai_v1beta3 as documentai

def extract_layout(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts layout elements (blocks, paragraphs, lines) from a document using Google Document AI.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Assuming PDF

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    
    layout_elements = {
        "pages": []
    }
    for page in result.document.pages:
        page_elements = {
            "page_number": page.page_number,
            "blocks": [page.get_text(block.layout) for block in page.blocks],
            "paragraphs": [page.get_text(para.layout) for para in page.paragraphs],
            "lines": [page.get_text(line.layout) for line in page.lines],
        }
        layout_elements["pages"].append(page_elements)

    return layout_elements

if __name__ == '__main__':
    # Placeholder for direct execution
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID_OCR") # A general OCR processor

    # Example: layout = extract_layout(project_id, location, processor_id, "path/to/your/document.pdf")
    # print("Extracted Layout:", layout)
