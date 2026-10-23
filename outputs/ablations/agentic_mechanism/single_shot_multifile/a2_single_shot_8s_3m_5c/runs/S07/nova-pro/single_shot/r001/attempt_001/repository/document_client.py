import os
from google.cloud import documentai_v1 as documentai

def ocr_client():
    client = documentai.DocumentProcessorServiceClient()
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    location = 'us'
    processor_id = '0000000000'  # Placeholder for a real processor ID
    processor = f'projects/{project_id}/locations/{location}/processors/{processor_id}'
    return client, processor