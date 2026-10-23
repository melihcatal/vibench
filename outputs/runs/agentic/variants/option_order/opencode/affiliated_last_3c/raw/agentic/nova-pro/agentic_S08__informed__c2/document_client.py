import os
from google.cloud import documentai


def get_client():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"
    return documentai.DocumentProcessorServiceClient()
