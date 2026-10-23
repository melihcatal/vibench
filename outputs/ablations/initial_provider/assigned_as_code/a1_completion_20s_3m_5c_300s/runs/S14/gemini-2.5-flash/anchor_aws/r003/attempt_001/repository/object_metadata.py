from storage_client import get_s3_client
from storage_models import ObjectMetadataPayload, ObjectMetadataResponse


def object_metadata(payload, config=None):
    config = config or {}
    client = get_s3_client(region_name=config.get("region"))
    object_name = payload["object_name"]

    response = client.head_object(Bucket=config["bucket"], Key=object_name)
    metadata = {
        "content_type": response.get("ContentType"),
        "last_modified": response.get("LastModified").isoformat() if response.get("LastModified") else None,
        "content_length": response.get("ContentLength"),
        **response.get("Metadata", {})
    }
    return ObjectMetadataResponse(object_name=object_name, metadata=metadata)
