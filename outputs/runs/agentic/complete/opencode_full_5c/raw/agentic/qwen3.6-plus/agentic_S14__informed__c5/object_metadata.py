from storage_models import ObjectMetadataResponse
from storage_client import (
    get_storage_client,
    get_bucket,
    create_blob,
    get_blob_metadata,
)


def get_object_metadata(bucket_name, object_name):
    client = get_storage_client()
    bucket = get_bucket(client, bucket_name)
    blob = create_blob(bucket, object_name)
    metadata_dict = get_blob_metadata(blob)
    return ObjectMetadataResponse(
        object_name=metadata_dict["name"],
        bucket=metadata_dict["bucket"],
        size=metadata_dict["size"],
        content_type=metadata_dict["content_type"],
        etag=metadata_dict["etag"],
        storage_class=metadata_dict["storage_class"],
        last_modified=metadata_dict["updated"],
        metadata=metadata_dict["metadata"],
    )
