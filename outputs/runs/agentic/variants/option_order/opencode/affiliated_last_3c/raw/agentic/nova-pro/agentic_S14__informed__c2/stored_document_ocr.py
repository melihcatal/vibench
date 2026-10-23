import os
from google.cloud import documentai_v1 as documentai

def stored_document_ocr(gcs_uri):
    client = documentai.DocumentProcessorServiceClient()
    project_id = 'YOUR_PROJECT_ID'
    location = 'YOUR_LOCATION'
    processor_id = 'YOUR_PROCESSOR_ID'
    processor = client.processor_path(project_id, location, processor_id)

    input_config = documentai.DocumentProcessorService
   .ProcessDocumentRequest
   .InputConfig(gcs_source=documentai.DocumentProcessorService
   .ProcessDocumentRequest.GcsSource(gcs_uri=gcs_uri))

    response = client.process_document(name=processor, input_config=input_config)

    for entity in response.entities:
        print(f"Entity: {entity.type_.name} {entity.mention_text}")
