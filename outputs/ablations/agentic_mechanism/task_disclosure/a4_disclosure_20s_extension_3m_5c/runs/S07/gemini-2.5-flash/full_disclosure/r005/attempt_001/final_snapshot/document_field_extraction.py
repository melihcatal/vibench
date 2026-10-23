from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions
import os

def extract_fields(project_id: str, location: str, processor_id: str, file_path: str, mime_type: str) -> dict:
    """
    Extracts structured fields from a document using Google Cloud Document AI.
    """
    # You can set the api_endpoint if you need to connect to a non-default region.
    # For example: client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # The full resource name of the processor
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type),
    )

    result = client.process_document(request=request)

    document = result.document
    
    # Extract form fields (key-value pairs)
    extracted_fields = []
    for page in document.pages:
        for form_field in page.form_fields:
            field_name = form_field.field_name.text_anchor.content if form_field.field_name.text_anchor else ""
            field_value = form_field.field_value.text_anchor.content if form_field.field_value.text_anchor else ""
            extracted_fields.append({
                "field_name": field_name.strip(),
                "field_value": field_value.strip()
            })
    return {"fields": extracted_fields}

