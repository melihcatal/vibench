import os
from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions


def get_documentai_client():
    # The Document AI client is configured with credentials using GOOGLE_APPLICATION_CREDENTIALS
    # For regional endpoints, set a client_options.api_endpoint value, e.g., "us-documentai.googleapis.com"
    # For this example, we'll use the default global endpoint.
    # client_options = ClientOptions(api_endpoint="us-documentai.googleapis.com")
    # client = documentai.DocumentProcessorServiceClient(client_options=client_options)
    client = documentai.DocumentProcessorServiceClient()
    return client
