from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import DocumentInput, DocumentField

PROJECT_ID = "YOUR_GOOGLE_CLOUD_PROJECT_ID"  # Replace with your project ID
LOCATION = "us"
PROCESSOR_ID = "YOUR_PROCESSOR_ID"  # e.g., "form-parser-v1-2020-09-23" or a custom processor for specific fields


def extract_document_fields(document_input: DocumentInput) -> List[DocumentField]:
    client = get_documentai_client()

    processor_name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

    raw_document = documentai.RawDocument(
        content=document_input.content, mime_type=document_input.mime_type
    )

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    response = client.process_document(request=request)

    document = response.document

    extracted_fields = []
    for entity in document.entities:
        # Assuming simple entity extraction for demonstration
        # More complex scenarios would involve traversing entity.properties for nested fields
        field_name = entity.type_
        field_value = document.text[
            entity.text_anchor.text_segments[
                0
            ].start_index : entity.text_anchor.text_segments[0].end_index
        ]
        confidence = entity.confidence
        extracted_fields.append(
            DocumentField(
                field_name=field_name, field_value=field_value, confidence=confidence
            )
        )

    # For form_parser processors, key-value pairs are usually in form_fields
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
            # Confidence for form fields might need to be derived or set to a default if not directly available
            extracted_fields.append(
                DocumentField(field_name=key, field_value=value, confidence=1.0)
            )  # Placeholder confidence

    return extracted_fields
