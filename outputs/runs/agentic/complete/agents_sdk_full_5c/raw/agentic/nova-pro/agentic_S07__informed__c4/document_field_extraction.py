from google.cloud import documentai

def extract_fields(image_path):
    client = documentai.DocumentProcessorServiceClient()
    with open(image_path, "rb") as image_file:
        image_content = image_file.read()
    document = {"content": image_content, "mime_type": "application/pdf"}
    request = {"name": "projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/processors/YOUR_PROCESSOR_ID", "document": document}
    response = client.process_document(request=request)
    fields = response.document.entities
    return fields