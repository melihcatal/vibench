import os
from google.cloud import documentai_v1 as documentai

def extract_key_values_from_document(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts key-value pairs from a form-like document using Google Document AI.
    This typically requires a FORM_PARSER type processor.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf",
        ),
    )

    result = client.process_document(request=request)
    document = result.document

    extracted_key_values = []

    for page in document.pages:
        for field in page.form_fields:
            key_text = documentai.Document.Page.Layout.text_anchor_to_text(field.field_name.text_anchor, document.text)
            value_text = documentai.Document.Page.Layout.text_anchor_to_text(field.field_value.text_anchor, document.text)
            extracted_key_values.append({"page_number": page.page_number, "key": key_text, "value": value_text})

    return extracted_key_values

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID_FORM_PARSER") # A FORM_PARSER type processor
    file_to_process = "path/to/your/form_document.pdf"

    if project_id and processor_id and os.path.exists(file_to_process):
        key_values_data = extract_key_values_from_document(project_id, location, processor_id, file_to_process)
        print("Extracted Key-Value Pairs:")
        import json
        print(json.dumps(key_values_data, indent=2))
    else:
        print("Please set GOOGLE_CLOUD_PROJECT, DOCUMENT_AI_PROCESSOR_ID_FORM_PARSER environment variables and ensure document file exists.")
