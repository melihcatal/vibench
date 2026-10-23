from google.cloud import documentai

def extract_receipt_fields(project_id, location, processor_id, file_path):
    client = documentai.DocumentProcessorServiceClient()
    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = {"content": image_content, "mime_type": 'application/pdf'}
    document = {"raw_document": raw_document}
    request = {"name": f'projects/{project_id}/locations/{location}/processors/{processor_id}', "document": document}

    result = client.process_document(request=request)
    document = result.document

    merchant = document.fields[0].value.string_value
    tax = document.fields[1].value.string_value
    total = document.fields[2].value.string_value
    items = [field.value.string_value for field in document.fields[3:]]

    return merchant, tax, total, items