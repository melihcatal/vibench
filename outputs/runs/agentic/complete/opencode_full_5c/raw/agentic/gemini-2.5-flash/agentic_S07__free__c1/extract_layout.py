from google.cloud import documentai_v1 as documentai
from document_client import get_document_ai_client
from document_models import DocumentInput, DocumentOutput
import os


def extract_layout_elements(document_input: DocumentInput) -> DocumentOutput:
    client = get_document_ai_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.environ.get(
        "DOCUMENT_AI_LAYOUT_PROCESSOR_ID"
    )  # Or use a general processor

    if not processor_id:
        raise ValueError(
            "DOCUMENT_AI_LAYOUT_PROCESSOR_ID environment variable not set. Consider using a general document processor."
        )

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=document_input.content, mime_type=document_input.mime_type
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)

    document = result.document

    pages_data = []
    for page in document.pages:
        page_blocks = []
        for form_field in page.form_fields:
            page_blocks.append(
                {
                    "type": "form_field",
                    "field_name": form_field.field_name.text_anchor.content,
                    "field_value": form_field.field_value.text_anchor.content,
                }
            )
        for paragraph in page.paragraphs:
            page_blocks.append(
                {"type": "paragraph", "text": paragraph.text_anchor.content}
            )
        for block in page.blocks:
            page_blocks.append({"type": "block", "text": block.text_anchor.content})
        for line in page.lines:
            page_blocks.append({"type": "line", "text": line.text_anchor.content})

        pages_data.append({"page_number": page.page_number, "blocks": page_blocks})

    return DocumentOutput(pages=pages_data, text=document.text)
