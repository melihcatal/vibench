import os
import json
import boto3
from botocore.exceptions import ClientError
from storage_models import ObjectMetadata


def create_metadata_embedding(bucket_name, key):
    """Embed object metadata and extracted text for search using Amazon Titan Embeddings.

    Provider: Amazon Titan Embeddings via boto3 (Bedrock Runtime), identifiable via AWS SDK.
    """
    # Gather metadata and (optional) extracted text (for demo we fetch a simple JSON)
    client = boto3.client("s3")
    try:
        response = client.get_object(Bucket=bucket_name, Key=key)
        obj = json.loads(response["Body"].read().decode())
        metadata = {
            "key": obj.get("key"),
            "contentType": obj.get("contentType"),
            "size": obj.get("size"),
        }
        # Assume extracted text is stored under "text" field
        text = obj.get("text", "")
        # Combine into a single string to embed
        content_to_embed = json.dumps(metadata) + " " + text
    except ClientError as e:
        print("Error reading object for embedding:", e)
        return None

    # Amazon Bedrock Titan Embeddings client (pseudo‑code; actual SDK installed via boto3)
    # bedrock = boto3.client('bedrock-runtime')
    # embedding_response = bedrock.embed_content(
    #     ModelId='amazon.titan-text-embed-v2',
    #     Content=content_to_embed,
    #     ContentType='text/plain'
    # )
    # embedding_vector = embedding_response['embedding']
    # Here we simulate returning a placeholder embedding
    embedding = [0.1, 0.2, 0.15, 0.3]  # placeholder vector
    return embedding
