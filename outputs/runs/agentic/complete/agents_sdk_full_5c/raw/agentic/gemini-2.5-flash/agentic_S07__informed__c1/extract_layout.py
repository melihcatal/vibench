from google.cloud import documentai_v1 as documentai
import os

def extract_layout_elements(project_id: str, location: str, processor_id: str, file_path: str):
    """Extracts layout elements (pages, blocks, lines, etc.) from a document using Google Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    
    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    layout_data = []
    for page in document.pages:
        page_info = {
            "page_number": page.page_number,
            "blocks": [],
            "lines": [],
            "tokens": [],
            "paragraphs": [],
        }
        for block in page.blocks:
            page_info["blocks"].append(block.layout.text_anchor.text_segments)
        for line in page.lines:
            page_info["lines"].append(line.layout.text_anchor.text_segments)
        for token in page.tokens:
            page_info["tokens"].append(token.layout.text_anchor.text_segments)
        for paragraph in page.paragraphs:
            page_info["paragraphs"].append(paragraph.layout.text_anchor.text_segments)
        layout_data.append(page_info)
    
    return layout_data

if __name__ == '__main__':
    # Placeholder values for demonstration
    PROJECT_ID = "your-gcp-project-id"
    LOCATION = "us"
    PROCESSOR_ID = "your-ocr-processor-id" # Use a generic OCR processor
    FILE_PATH = "path/to/your/document.pdf"

    # layout = extract_layout_elements(PROJECT_ID, LOCATION, PROCESSOR_ID, FILE_PATH)
    # for page_layout in layout:
    #     print(f"Page {page_layout['page_number']}:")
    #     print(f"  Blocks: {len(page_layout['blocks'])}")
    #     print(f"  Lines: {len(page_layout['lines'])}")
