from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import DocumentInput, ExtractedKeyValue

PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID"  # Replace with your project ID
LOCATION = "us"
PROCESSOR_ID = "YOUR_FORM_PARSER_PROCESSOR_ID"  # e.g., "form-parser-v1-2020-09-23"


def extract_key_values_from_document(
    document_input: DocumentInput,
) -> List[ExtractedKeyValue]:
    client = get_documentai_client()

    processor_name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

    raw_document = documentai.RawDocument(
        content=document_input.content, mime_type=document_input.mime_type
    )

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    response = client.process_document(request=request)

    document = response.document

    key_value_pairs = []
    for page in document.pages:
        for form_field in page.form_fields:
            key = document.text[
                form_field.field_name.text_anchor.text_segments[
                    0
                ].start_index : form_field.field_name.text_anchor.text_segments[
                    0
                ].end_index
            ]
            value = document.text[
                form_field.field_value.text_anchor.text_segments[
                    0
                ].start_index : form_field.field_value.text_anchor.text_segments[
                    0
                ].end_index
            ]
            key_value_pairs.append(ExtractedKeyValue(key=key, value=value))

    return key_value_pairs
