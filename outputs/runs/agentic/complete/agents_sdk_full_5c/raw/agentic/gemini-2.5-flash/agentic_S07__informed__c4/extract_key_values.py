import os
from google.cloud import documentai_v1beta3 as documentai

def extract_key_values_from_document(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts key-value pairs from a form-like document using Google Document AI.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # Assuming PDF for simplicity

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)

    document = result.document
    # Form fields (key-value pairs) are usually found in document.entities
    return document.entities

if __name__ == '__main__':
    # Placeholder for actual usage, demonstrating the provider integration
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us" # e.g., "us"
    processor_id = os.environ.get("DOCUMENTAI_FORM_PROCESSOR_ID") # e.g., a specific form parser processor ID
    file_to_process = "path/to/your/form_document.pdf" # Replace with your document path

    if project_id and processor_id and os.path.exists(file_to_process):
        print(f"Extracting key-value pairs from {file_to_process} using Google Document AI...")
        # entities = extract_key_values_from_document(project_id, location, processor_id, file_to_process)
        # for entity in entities:
        #     if entity.type_ == "form_field": # or other relevant entity types
        #         print(f"Key: {entity.normalized_value.text if entity.normalized_value else entity.text_anchor.content}, Value: {entity.normalized_value.text if entity.normalized_value else ''}")
    else:
        print("Please set GOOGLE_CLOUD_PROJECT, DOCUMENTAI_FORM_PROCESSOR_ID environment variables and ensure the file exists.")
