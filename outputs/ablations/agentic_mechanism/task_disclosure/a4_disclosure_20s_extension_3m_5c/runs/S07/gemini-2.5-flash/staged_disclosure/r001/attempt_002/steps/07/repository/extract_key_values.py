import io
from google.cloud import documentai_v1 as documentai

def extract_key_values_from_document(project_id: str, location: str, processor_id: str, file_path: str):
    client = documentai.DocumentProcessorServiceClient()
    resource_name = client.processor_path(project_id, location, processor_id)
    with open(file_path, "rb") as image:
        image_content = image.read()
    request = documentai.ProcessRequest(
        name=resource_name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf",
        ),
    )
    result = client.process_document(request=request)
    document = result.document
    key_value_pairs = {}
    for page in document.pages:
        for form_field in page.form_fields:
            key = form_field.field_name.text_anchor.content
            value = form_field.field_value.text_anchor.content
            key_value_pairs[key.strip()] = value.strip()
    return key_value_pairs