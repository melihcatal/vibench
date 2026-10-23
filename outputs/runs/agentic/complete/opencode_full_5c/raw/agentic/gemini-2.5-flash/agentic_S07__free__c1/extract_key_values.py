from google.cloud import documentai_v1 as documentai
from document_client import get_document_ai_client
from document_models import DocumentInput, DocumentOutput
import os


def extract_key_value_pairs(document_input: DocumentInput) -> DocumentOutput:
    client = get_document_ai_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.environ.get(
        "DOCUMENT_AI_FORM_PROCESSOR_ID"
    )  # Use a form parser or general processor

    if not processor_id:
        raise ValueError(
            "DOCUMENT_AI_FORM_PROCESSOR_ID environment variable not set. Consider using a general document processor or a specific form processor."
        )

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=document_input.content, mime_type=document_input.mime_type
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)

    document = result.document

    key_value_pairs = []
    for page in document.pages:
        for form_field in page.form_fields:
            key_value_pairs.append(
                {
                    "field_name": form_field.field_name.text_anchor.content,
                    "field_value": form_field.field_value.text_anchor.content,
                    "page_number": page.page_number,
                }
            )

    return DocumentOutput(key_value_pairs=key_value_pairs, text=document.text)
