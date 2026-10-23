from google.cloud import documentai


def extract_fields(text, config):
    client = documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": f"{config['location']}-documentai.googleapis.com"})
    name = client.processor_path(config["project_id"], config["location"], config["processor_id"])
    response = client.process_document(request={
        "name": name,
        "raw_document": documentai.RawDocument(
            content=text.encode('utf-8'), mime_type="text/plain")
    })
    fields = {}
    for page in response.document.pages:
        for key_value_pair in page.key_value_pairs:
            key = key_value_pair.key.text
            value = key_value_pair.value.text
            fields[key] = value
    return fields