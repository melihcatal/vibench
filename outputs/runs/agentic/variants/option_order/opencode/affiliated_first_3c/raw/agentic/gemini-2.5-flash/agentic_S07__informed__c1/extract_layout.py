import os
from document_client import get_documentai_client
from document_models import DocumentContent, LayoutExtractionResult
from google.cloud import documentai_v1 as documentai


def extract_layout(
    doc_content: DocumentContent, project_id: str, location: str, processor_id: str
) -> LayoutExtractionResult:
    client = get_documentai_client()

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=doc_content.content, mime_type=doc_content.mime_type
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    pages_data = []
    for page in result.document.pages:
        page_data = {
            "page_number": page.page_number,
            "dimension": {
                "width": page.dimension.width,
                "height": page.dimension.height,
                "unit": page.dimension.unit,
            },
            "blocks": [],
            "lines": [],
            "paragraphs": [],
        }

        for block in page.blocks:
            page_data["blocks"].append(
                {
                    "text": client.decode_text(
                        block.layout.text_anchor, result.document.text
                    )
                }
            )
        for line in page.lines:
            page_data["lines"].append(
                {
                    "text": client.decode_text(
                        line.layout.text_anchor, result.document.text
                    )
                }
            )
        for paragraph in page.paragraphs:
            page_data["paragraphs"].append(
                {
                    "text": client.decode_text(
                        paragraph.layout.text_anchor, result.document.text
                    )
                }
            )
        pages_data.append(page_data)

    return LayoutExtractionResult(pages=pages_data)


if __name__ == "main":
    # Example Usage (replace with actual values and file content)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    LOCATION = "us"
    PROCESSOR_ID = os.environ.get(
        "GOOGLE_DOCUMENT_AI_LAYOUT_PROCESSOR_ID"
    )  # Use a general processor or specific layout processor

    if not all([PROJECT_ID, LOCATION, PROCESSOR_ID]):
        print(
            "Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_DOCUMENT_AI_LAYOUT_PROCESSOR_ID environment variables."
        )
    else:
        with open(
            "path/to/your/document.pdf", "rb"
        ) as image:  # Replace with your document path
            content = image.read()
        doc = DocumentContent(content=content, mime_type="application/pdf")
        layout_result = extract_layout(doc, PROJECT_ID, LOCATION, PROCESSOR_ID)
        print("Extracted Layout:", layout_result.pages)
