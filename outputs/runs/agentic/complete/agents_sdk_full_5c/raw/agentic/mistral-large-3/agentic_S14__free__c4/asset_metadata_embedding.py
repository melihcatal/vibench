import boto3
import json
from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest

def embed_asset_metadata(bucket_name: str, object_key: str) -> dict:
    s3_client = get_storage_client()
    bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

    try:
        metadata_response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        metadata = metadata_response.get('Metadata', {})
        content_type = metadata_response.get('ContentType', '')

        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        text = response['Body'].read().decode('utf-8') if content_type.startswith('text/') else ""

        combined_text = f"Metadata: {json.dumps(metadata)}\nContent: {text}"
        body = {
            "inputText": combined_text,
            "textGenerationConfig": {
                "maxTokenCount": 4096,
                "temperature": 0.0
            }
        }

        bedrock_response = bedrock_client.invoke_model(
            modelId="amazon.titan-embed-text-v1",
            body=bytes(json.dumps(body), 'utf-8')
        )
        embedding = json.loads(bedrock_response['body'].read().decode('utf-8'))['embedding']

        return {
            "bucket_name": bucket_name,
            "object_key": object_key,
            "embedding": embedding,
            "success": True
        }
    except Exception as e:
        return {
            "bucket_name": bucket_name,
            "object_key": object_key,
            "success": False,
            "error": str(e)
        }