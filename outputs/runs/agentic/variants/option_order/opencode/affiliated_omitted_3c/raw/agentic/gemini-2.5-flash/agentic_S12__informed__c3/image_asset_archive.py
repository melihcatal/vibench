from vision_client import VisionClient


def archive_image_asset(bucket_name: str, object_key: str, data: bytes) -> dict:
    s3_client = VisionClient().get_s3_client()
    response = s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=data)
    return response


def archive_text_asset(bucket_name: str, object_key: str, text_content: str) -> dict:
    s3_client = VisionClient().get_s3_client()
    response = s3_client.put_object(
        Bucket=bucket_name, Key=object_key, Body=text_content.encode("utf-8")
    )
    return response
