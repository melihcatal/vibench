from google.cloud import documentai
from document_client import get_documentai_client

def extract_layout(payload, config=None):
    config = config or {}
    client = get_documentai_client(config['location'])
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"])})
    
    # The response.document object contains various layout elements like pages, blocks, paragraphs, etc.
    # For simplicity, we'll return a dictionary representation of some layout elements.
    # A more detailed implementation would parse and structure this data as needed.
    layout_info = []
    for page in response.document.pages:
        page_layout = {
            "page_number": page.page_number,
            "blocks": [block.layout.text_anchor.text_segments[0].start_index for block in page.blocks if block.layout.text_anchor.text_segments], # Example: just start index
            "paragraphs": [paragraph.layout.text_anchor.text_segments[0].start_index for paragraph in page.paragraphs if paragraph.layout.text_anchor.text_segments],
            "lines": [line.layout.text_anchor.text_segments[0].start_index for line in page.lines if line.layout.text_anchor.text_segments],
        }
        layout_info.append(page_layout)

    return {"layout_info": layout_info, "full_text": response.document.text}
