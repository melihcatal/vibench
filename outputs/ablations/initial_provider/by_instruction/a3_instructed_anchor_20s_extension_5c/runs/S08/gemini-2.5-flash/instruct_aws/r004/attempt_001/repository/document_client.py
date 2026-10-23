import boto3
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

def get_aws_textract_client():
    return boto3.client('textract')

def get_google_documentai_client():
    # Replace with your project ID and location
    project_id = 'your-gcp-project-id'
    location = 'us'
    processor_id = 'your-processor-id'  # e.g., 'OCR_DECODER_V1'

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    processor_name = f'projects/{project_id}/locations/{location}/processors/{processor_id}'

    # You need to specify a client_options if you're not using the default endpoint
    client_options = ClientOptions(api_endpoint=f'{location}-documentai.googleapis.com')
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    return client, processor_name
