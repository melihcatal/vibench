import os
import google.cloud.documentai as documentai


def get_document_client():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"
    return documentai.DocumentProcessorClient()
