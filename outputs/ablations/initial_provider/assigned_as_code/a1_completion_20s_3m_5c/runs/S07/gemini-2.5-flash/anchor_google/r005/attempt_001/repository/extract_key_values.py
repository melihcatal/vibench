from google.cloud import documentai
from document_client import get_documentai_client

def extract_key_values(payload, config=None):
    config = config or {}
    client = get_documentai_client(config['location'])
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={"name": name, "raw_document": documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"])})
    
    key_value_pairs = []
    for page in response.document.pages:
        for form_field in page.form_fields:
            key = response.document.text[form_field.field_name.text_segments[0].start_index:form_field.field_name.text_segments[0].end_index]
            value = response.document.text[form_field.field_value.text_segments[0].start_index:form_field.field_value.text_segments[0].end_index]
            key_value_pairs.append({"key": key, "value": value, "page_number": page.page_number})

    return {"key_value_pairs": key_value_pairs, "full_text": response.document.text}
