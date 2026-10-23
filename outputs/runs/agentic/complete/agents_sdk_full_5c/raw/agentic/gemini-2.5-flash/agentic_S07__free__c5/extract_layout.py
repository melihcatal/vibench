import os
from google.cloud import documentai_v1 as documentai

def extract_layout(project_id: str, location: str, processor_id: str, file_content: bytes, mime_type: str) -> dict:
    """Extracts layout elements (blocks, lines, tables) from a document using Google Cloud Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    processor_name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=file_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    # For simplicity, returning a dictionary representation of some layout elements
    # A more robust solution would parse specific layout components as needed.
    layout_data = {
        "text": document.text,
        "pages": []
    }

    for page in document.pages:
        page_data = {
            "page_number": page.page_number,
            "blocks": [],
            "lines": [],
            "tokens": []
        }
        for block in page.blocks:
            page_data["blocks"].append({"text_anchor": {"text_segments": [{"start_index": block.layout.text_anchor.text_segments[0].start_index, "end_index": block.layout.text_anchor.text_segments[0].end_index}]} if block.layout.text_anchor.text_segments else {}})
        for line in page.lines:
            page_data["lines"].append({"text_anchor": {"text_segments": [{"start_index": line.layout.text_anchor.text_segments[0].start_index, "end_index": line.layout.text_anchor.text_segments[0].end_index}]} if line.layout.text_anchor.text_segments else {}})
        for token in page.tokens:
            page_data["tokens"].append({"text_anchor": {"text_segments": [{"start_index": token.layout.text_anchor.text_segments[0].start_index, "end_index": token.layout.text_anchor.text_segments[0].end_index}]} if token.layout.text_anchor.text_segments else {}})
        layout_data["pages"].append(page_data)

    return layout_data

if __name__ == '__main__':
    # Example usage (replace with your actual project, location, processor, and file)
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # location = "us"  # e.g., "us" or "eu"
    # processor_id = "YOUR_PROCESSOR_ID" # e.g., a "Form Parser" processor
    #
    # if project_id and processor_id:
    #     with open("path/to/your/document.pdf", "rb") as doc_file:
    #         content = doc_file.read()
    #         mime_type = "application/pdf"
    #         layout_info = extract_layout(project_id, location, processor_id, content, mime_type)
    #         print("Extracted Layout:", layout_info)
    # else:
    #     print("Please set GOOGLE_CLOUD_PROJECT and provide a processor_id.")
    pass
