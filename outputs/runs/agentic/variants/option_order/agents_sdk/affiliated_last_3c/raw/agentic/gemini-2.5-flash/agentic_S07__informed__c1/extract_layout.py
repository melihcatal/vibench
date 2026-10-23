import os
from google.cloud import documentai_v1 as documentai

def extract_layout_from_document(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts layout elements (blocks, lines, tables) from a document using Google Document AI.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf",
        ),
    )

    result = client.process_document(request=request)
    document = result.document

    layout_info = {
        "pages": []
    }

    for page in document.pages:
        page_data = {
            "page_number": page.page_number,
            "blocks": [],
            "lines": [],
            "tokens": [],
            "form_fields": [],
            "tables": []
        }

        for block in page.blocks:
            page_data["blocks"].append(documentai.Document.Page.Layout.text_anchor_to_text(block.layout.text_anchor, document.text))

        for line in page.lines:
            page_data["lines"].append(documentai.Document.Page.Layout.text_anchor_to_text(line.layout.text_anchor, document.text))

        for token in page.tokens:
            page_data["tokens"].append(documentai.Document.Page.Layout.text_anchor_to_text(token.layout.text_anchor, document.text))
        
        # Add form fields and tables later when processing specific elements

        layout_info["pages"].append(page_data)

    return layout_info

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID_OCR") # A "FORM_PARSER" or "OCR_PROCESSOR" type processor
    file_to_process = "path/to/your/document.pdf"

    if project_id and processor_id and os.path.exists(file_to_process):
        layout_data = extract_layout_from_document(project_id, location, processor_id, file_to_process)
        print("Extracted Layout Info:")
        import json
        print(json.dumps(layout_data, indent=2))
    else:
        print("Please set GOOGLE_CLOUD_PROJECT, DOCUMENT_AI_PROCESSOR_ID_OCR environment variables and ensure document file exists.")
