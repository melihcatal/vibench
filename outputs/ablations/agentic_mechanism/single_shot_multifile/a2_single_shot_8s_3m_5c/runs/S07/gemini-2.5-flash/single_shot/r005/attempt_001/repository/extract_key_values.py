import os
from google.cloud import documentai_v1 as documentai
from document_client import get_document_ai_client
from document_models import DocumentKeyValue

def extract_key_value_pairs(image_content: bytes, mime_type: str = "application/pdf") -> list[DocumentKeyValue]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")
    processor_id = os.environ.get("GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID_FORMS")

    if not all([project_id, location, processor_id]):
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT_ID, GOOGLE_CLOUD_LOCATION, or GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID_FORMS environment variables.")

    processor_name = client.processor_path(project_id, location, processor_id)
    client = get_document_ai_client()

    document = documentai.Document(content=image_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, document=document)

    response = client.process_document(request=request)

    key_value_pairs = []
    if response.document and response.document.entities:
        for entity in response.document.entities:
            if entity.type_ == "form_field": # This is a common type for key-value pairs
                key_text = response.document.text[entity.text_anchor.text_segments[0].start_index:entity.text_anchor.text_segments[0].end_index] if entity.text_anchor.text_segments else ""
                value_text = ""
                if entity.properties:
                    # For form fields, the 'value' is often a property of the main entity
                    for prop in entity.properties:
                        if prop.type_ == "value": # Assuming 'value' is the property holding the actual value
                             value_text = response.document.text[prop.text_anchor.text_segments[0].start_index:prop.text_anchor.text_segments[0].end_index] if prop.text_anchor.text_segments else ""
                             break
                elif entity.mention_text: # Fallback if properties not structured as expected
                     value_text = entity.mention_text

                key_value_pairs.append(DocumentKeyValue(key=key_text, value=value_text))

    return key_value_pairs
