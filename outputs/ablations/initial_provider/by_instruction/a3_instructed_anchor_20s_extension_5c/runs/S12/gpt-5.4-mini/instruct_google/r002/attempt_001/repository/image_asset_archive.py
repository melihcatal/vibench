from vision_client import archive_payload


def image_asset_archive(bucket_name: str, object_name: str, payload: str) -> str:
    return archive_payload(bucket_name, object_name, payload)
