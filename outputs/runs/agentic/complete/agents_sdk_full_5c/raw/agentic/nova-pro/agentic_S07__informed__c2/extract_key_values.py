from google.cloud import documentai

def extract_key_values(project_id, location, processor_id, file_path):
    client = documentai.DocumentProcessorServiceClient()
    with open(file_path, "rb") as image:
        image_content = image.read()

    image = documentai.RawDocument(content=image_content)
    name = f'projects/{project_id}/locations/{location}/processors/{processor_id}'
    response = client.process_document(name=name, raw_document=image)
    return response.document.entities