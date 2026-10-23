import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from mindee import MindeeClient, doc_types
import boto3
import requests

# Common helpers
ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
MINDEE_API_KEY = os.getenv("MINDEE_API_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Provider‑specific clients
DOC_CLIENT = DocumentIntelligenceClient(
    endpoint=ENDPOINT, credential=AzureKeyCredential(KEY)
) if ENDPOINT and KEY else None

MINDEE_CLIENT = MindeeClient(api_key=MINDEE_API_KEY) if MINDEE_API_KEY else None

S3_CLIENT = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
) if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY else None

def upload_to_azure_blob(container_name, blob_name, document_bytes):
    """Upload a document to Azure Blob Storage (requires Azure SDK)."""
    from azure.storage.blob import BlobServiceClient
    blob_service = BlobServiceClient.from_connection_string(
        os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    )
    container_client = blob_service.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(document_bytes)


def upload_to_mindee(bucket_name, object_key, image_bytes):
    """Upload receipt image to Mindee storage (if needed)."""
    # Mindee does not expose a public upload endpoint; this is a placeholder for
    # integration with Mindee's S3 bucket for custom receipt models.
    S3_CLIENT.upload_fileobj(
        io.BytesIO(image_bytes),
        bucket_name,
        object_key,
    )
