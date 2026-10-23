from google.cloud import documentai

def extract_fields(document_path):
    client = documentai.DocumentProcessorServiceClient()
    gcs_source_uri = 'gs://YOUR_BUCKET_NAME/{}'.format(document_path)
    input_config = documentai.DocumentProcessorService.types.InputConfig(
        gcs_source=documentai.DocumentProcessorService.types.GcsSource(
            uris=[gcs_source_uri]))
    response = client.process_document(name='projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/processors/YOUR_PROCESSOR_ID',
                                      input_config=input_config)
    document = response.document
    fields = {entity.type_: entity.mention_text for entity in document.entities}
    return fields