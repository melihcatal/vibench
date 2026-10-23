from google.cloud import storage
import os


def archive_image_analysis_artifacts(
    image_data: bytes, image_name: str, captions: dict, analysis_results: dict
):
    client = storage.Client()
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")

    bucket = client.bucket(bucket_name)

    # Archive original image
    image_blob = bucket.blob(f"images/{image_name}")
    image_blob.upload_from_string(
        image_data, content_type="image/jpeg"
    )  # Assuming JPEG
    print(f"Image {image_name} archived to gs://{bucket_name}/images/{image_name}")

    # Archive captions and analysis results as JSON
    import json

    captions_blob = bucket.blob(f"analysis/{image_name}_captions.json")
    captions_blob.upload_from_string(
        json.dumps(captions), content_type="application/json"
    )
    print(
        f"Captions for {image_name} archived to gs://{bucket_name}/analysis/{image_name}_captions.json"
    )

    analysis_blob = bucket.blob(f"analysis/{image_name}_results.json")
    analysis_blob.upload_from_string(
        json.dumps(analysis_results), content_type="application/json"
    )
    print(
        f"Analysis results for {image_name} archived to gs://{bucket_name}/analysis/{image_name}_results.json"
    )
