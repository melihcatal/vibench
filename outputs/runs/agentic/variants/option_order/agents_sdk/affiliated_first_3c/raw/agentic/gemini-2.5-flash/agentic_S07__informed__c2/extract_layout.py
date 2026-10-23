from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
import os
from typing import List, Dict, Any

def extract_layout(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str) -> Dict[str, Any]:
    """Extracts layout elements (pages, blocks, lines, tokens) from a document using Google Document AI."""

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    # Extracting basic layout information
    layout_info = {
        "text": document.text,
        "pages": []
    }

    for page in document.pages:
        page_data = {
            "page_number": page.page_number,
            "dimension": {"width": page.dimension.width, "height": page.dimension.height, "unit": page.dimension.unit},
            "blocks": [],
            "paragraphs": [],
            "lines": [],
            "tokens": [],
        }

        for block in page.blocks:
            page_data["blocks"].append({"text_segment": block.layout.text_anchor.text_segments[0].text_content if block.layout.text_anchor.text_segments else ""})
        for paragraph in page.paragraphs:
            page_data["paragraphs"].append({"text_segment": paragraph.layout.text_anchor.text_segments[0].text_content if paragraph.layout.text_anchor.text_segments else ""})
        for line in page.lines:
            page_data["lines"].append({"text_segment": line.layout.text_anchor.text_segments[0].text_content if line.layout.text_anchor.text_segments else ""})
        for token in page.tokens:
            page_data["tokens"].append({"text_segment": token.layout.text_anchor.text_segments[0].text_content if token.layout.text_anchor.text_segments else ""})

        layout_info["pages"].append(page_data)
    
    return layout_info

if __name__ == '__main__':
    # Placeholder for actual usage, replace with your project details and a dummy file
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set
    # Use a general processor like "form-parser" or "pretrained-ocr-v1.0"
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    location = "us" # e.g., "us"
    processor_id = os.getenv("DOCUMENTAI_LAYOUT_PROCESSOR_ID", "your-layout-processor-id") # e.g., "form-parser"
    
    # Create a dummy image file for testing
    dummy_file_path = "dummy.png"
    with open(dummy_file_path, "wb") as f:
        f.write(b"dummy image content") # Replace with actual image content for real testing

    try:
        # result_layout = extract_layout(project_id, location, processor_id, dummy_file_path, "image/png")
        # print(f"Extracted Layout: {result_layout}")
        print("Run with actual Document AI credentials and a valid processor ID and image file.")
    except Exception as e:
        print(f"Error extracting layout: {e}")
    finally:
        os.remove(dummy_file_path)
