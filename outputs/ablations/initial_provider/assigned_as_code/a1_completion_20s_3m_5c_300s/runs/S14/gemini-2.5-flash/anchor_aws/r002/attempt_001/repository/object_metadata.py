import boto3
from storage_client import get_s3_client
from storage_models import ObjectMetadataRequest

def get_object_metadata(payload: ObjectMetadataRequest, config: dict = None) -> dict:
    config = config or {}
    s3_client = get_s3_client(config)
    
    response = s3_client.head_object(Bucket=config["bucket"], Key=payload.object_name)
    return {"metadata": response.get("Metadata"), "content_type": response.get("ContentType")}
