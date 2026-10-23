from google.cloud import documentai_v1 as documentai
import os


def extract_layout(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts layout elements (pages, blocks, lines, etc.) from a document using Google Document AI.
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

    document_layout = {"pages": []}
    for page in result.document.pages:
        page_info = {
            "page_number": page.page_number,
            "blocks": [],
            "lines": [],
            "tokens": [],
        }
        for block in page.blocks:
            page_info["blocks"].append(
                block.layout.text_anchor.text_segments[0].text_content
                if block.layout.text_anchor.text_segments
                else ""
            )
        for line in page.lines:
            page_info["lines"].append(
                line.layout.text_anchor.text_segments[0].text_content
                if line.layout.text_anchor.text_segments
                else ""
            )
        for token in page.tokens:
            page_info["tokens"].append(
                token.layout.text_anchor.text_segments[0].text_content
                if token.layout.text_anchor.text_segments
                else ""
            )
        document_layout["pages"].append(page_info)

    return document_layout


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"  # e.g., "us"
    processor_id = os.environ.get(
        "GOOGLE_DOCUMENT_AI_PROCESSOR_ID"
    )  # e.g., "YOUR_PROCESSOR_ID"
    file_path = "path/to/your/document.pdf"  # Replace with your document path
    # layout = extract_layout(project_id, location, processor_id, file_path)
    # import json
    # print(json.dumps(layout, indent=2))
