def create_request(project_id, location, processor_id, file_path):
    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = {"content": image_content, "mime_type": 'application/pdf'}
    document = {"raw_document": raw_document}
    request = {"name": f'projects/{project_id}/locations/{location}/processors/{processor_id}', "document": document}
    return request

def parse_response(response):
    document = response.document
    fields = {}
    for field in document.fields:
        fields[field.field_name] = field.value.string_value
    return fields