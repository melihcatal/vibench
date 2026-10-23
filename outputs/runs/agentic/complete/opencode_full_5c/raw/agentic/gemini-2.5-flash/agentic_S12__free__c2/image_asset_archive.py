from vision_client import VisionClient
import json


def archive_image_analysis_artifact(bucket_name, destination_blob_name, data):
    client = VisionClient().storage_client
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Data can be a string, bytes, or file-like object.
    # Assuming 'data' is a dictionary containing analysis results, we'll convert it to JSON.
    blob.upload_from_string(json.dumps(data), content_type="application/json")

    return {
        "status": "success",
        "blob_path": f"gs://{bucket_name}/{destination_blob_name}",
    }


def archive_image_asset(bucket_name, destination_blob_name, image_content):
    client = VisionClient().storage_client
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(image_content)

    return {
        "status": "success",
        "blob_path": f"gs://{bucket_name}/{destination_blob_name}",
    }
