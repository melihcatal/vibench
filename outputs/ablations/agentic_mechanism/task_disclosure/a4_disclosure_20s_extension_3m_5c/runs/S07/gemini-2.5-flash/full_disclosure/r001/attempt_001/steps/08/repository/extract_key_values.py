import os
from google.cloud import documentai_v1beta3 as documentai

def extract_key_values(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts key-value pairs from a form-like document using Google Cloud Document AI.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type="application/pdf" # Assuming PDF, adjust as needed
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    key_value_pairs = []
    for page in document.pages:
        for form_field in page.form_fields:
            field_name = form_field.field_name.text_anchor.content
            field_value = form_field.field_value.text_anchor.content
            key_value_pairs.append({
                "field_name": field_name.strip(),
                "field_value": field_value.strip()
            })
    return key_value_pairs
