import os
from google.cloud import documentai_v1 as documentai
import boto3

def get_documentai_client():
    """Returns a Google Cloud Document AI client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    return documentai.DocumentProcessorServiceClient()

def get_textract_client():
    """Returns an AWS Textract client."""
    # Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set.
    return boto3.client('textract', region_name='us-east-1') # Specify a region
