from google.cloud import documentai_v1beta3 as documentai
import os


def get_documentai_client():
    """
    Returns a Google Document AI client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    return documentai.DocumentProcessorServiceClient()
