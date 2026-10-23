import os
import json
from google.cloud import storage
from vision_models import ImageAnalysisResult, ArchiveResult

def archive_image_analysis(image_local_path: str, analysis_result: ImageAnalysisResult, bucket_name: str, destination_blob_prefix: str) -> ArchiveResult:
    """Archives the original image and its analysis results to Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Upload the original image
    image_blob_name = f"{destination_blob_prefix}/{os.path.basename(image_local_path)}"
    image_blob = bucket.blob(image_blob_name)
    image_blob.upload_from_filename(image_local_path)
    print(f"Image {image_local_path} uploaded to gs://{bucket_name}/{image_blob_name}")

    # Upload the analysis results as a JSON file
    metadata_blob_name = f"{destination_blob_prefix}/{os.path.basename(image_local_path)}.json"
    metadata_blob = bucket.blob(metadata_blob_name)
    
    # Convert dataclass to dictionary for JSON serialization
    analysis_dict = {
        "image_uri": analysis_result.image_uri,
        "labels": analysis_result.labels,
        "description": analysis_result.description,
        "detected_text": analysis_result.detected_text,
        "safety_scores": analysis_result.safety_scores
    }
    metadata_blob.upload_from_string(json.dumps(analysis_dict), content_type="application/json")
    print(f"Analysis results uploaded to gs://{bucket_name}/{metadata_blob_name}")

    return ArchiveResult(
        image_uri=analysis_result.image_uri,
        archive_location=f"gs://{bucket_name}/{image_blob_name}",
        metadata_location=f"gs://{bucket_name}/{metadata_blob_name}"
    )

if __name__ == '__main__':
    # Example usage for demonstration
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set and you have a GCS bucket.
    # Create a dummy image file for testing
    dummy_image_path = "dummy_image_to_archive.jpg"
    if not os.path.exists(dummy_image_path):
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (100, 50), color = 'blue')
        d = ImageDraw.Draw(img)
        d.text((10,10), "Archive Me!", fill=(255,255,255))
        img.save(dummy_image_path)
        print(f"Created a dummy image: {dummy_image_path}")

    example_analysis = ImageAnalysisResult(
        image_uri="gs://source-bucket/original.jpg",
        labels=["test", "archive"],
        description="A test image for archiving.",
        detected_text=["Archive Me!"],
        safety_scores={'adult': 'VERY_UNLIKELY'}
    )

    bucket_name = os.environ.get("GCS_BUCKET_NAME") # Replace with your GCS bucket name
    if not bucket_name:
        print("Error: GCS_BUCKET_NAME environment variable not set. Cannot run example.")
    else:
        try:
            destination_prefix = "image_analysis_archives/test_run"
            print(f"Archiving image and analysis to gs://{bucket_name}/{destination_prefix}")
            archive_results = archive_image_analysis(
                image_local_path=dummy_image_path,
                analysis_result=example_analysis,
                bucket_name=bucket_name,
                destination_blob_prefix=destination_prefix
            )
            print("\nArchive Results:")
            print(archive_results)
        except Exception as e:
            print(f"Error archiving assets: {e}")
            print("Please ensure GOOGLE_APPLICATION_CREDENTIALS is set and GCS_BUCKET_NAME is valid.")
