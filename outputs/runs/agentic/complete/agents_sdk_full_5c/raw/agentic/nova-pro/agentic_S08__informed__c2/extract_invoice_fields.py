from google.cloud import documentai

def extract_invoice_fields(project_id, location, processor_id, file_path):
    client = documentai.DocumentProcessorServiceClient()
    with open(file_path, "rb") as image:
        image_content = image.read()
    document = {"content": image_content, "mime_type": 'application/pdf'}
    request = {"name": f'projects/{project_id}/locations/{location}/processors/{processor_id}',
                "document": document}
    result = client.process_document(request=request)
    return result.document