import boto3
import embeddings

from storage_client import get_s3_client


def embed_asset_metadata(object_name):
    client = get_s3_client()
    response = client.get_object(Bucket='your-bucket-name', Key=object_name)
    metadata = response['Metadata']
    extracted_text = response['Body'].read().decode('utf-8')
    # Embed metadata and extracted text
    # This is a placeholder for actual embedding implementation
    return 'Embedded metadata and text'