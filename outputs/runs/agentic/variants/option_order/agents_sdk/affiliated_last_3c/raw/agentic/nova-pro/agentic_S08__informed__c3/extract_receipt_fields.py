from google.cloud import documentai

def extract_receipt_fields(document_path):
    client = documentai.DocumentProcessorServiceClient()
    with open(document_path, 'rb') as image_file:
        content = image_file.read()
    image = documentai.DocumentImage(content=content)
    response = client.process_document(name='projects/your-project-id/locations/your-location/processors/your-processor-id', document={'image': image})
    # Extract fields from response
    return extracted_fields