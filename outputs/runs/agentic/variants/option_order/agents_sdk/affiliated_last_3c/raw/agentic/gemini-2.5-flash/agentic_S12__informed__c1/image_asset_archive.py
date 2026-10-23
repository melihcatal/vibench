from google.cloud import storage
import os
import json
from typing import Dict, Any

def archive_image_analysis_artifacts(bucket_name: str, object_name: str, data: Dict[str, Any]):
    """Archives image analysis artifacts and derived captions in Google Cloud Storage.

    Args:
        bucket_name: The name of the GCS bucket.
        object_name: The name of the object to create/update (e.g., path/to/analysis_results.json).
        data: A dictionary containing the analysis results to be stored.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    # Example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please set it to the path of your service account key file for authentication.")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    try:
        # Convert data dictionary to a JSON string and upload
        json_data = json.dumps(data, indent=2)
        blob.upload_from_string(json_data, content_type='application/json')
        print(f"Archived analysis results to gs://{bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error archiving analysis results: {e}")

if __name__ == '__main__':
    # Example usage
    # Set your GOOGLE_APPLICATION_CREDENTIALS environment variable before running
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    
    # Replace with your actual bucket name and desired object name
    my_bucket_name = "your-gcs-bucket-name"
    my_object_name = "image_analysis_archives/image_123_results.json"

    sample_analysis_data = {
        "image_uri": "gs://cloud-samples-data/vision/label/wakeupcat.jpg",
        "labels": ["cat", "animal", "sleep"],
        "description": "An image of a cat sleeping.",
        "detected_text": "",
        "safety_scores": {
            "adult": "VERY_UNLIKELY",
            "violence": "UNLIKELY"
        },
        "summary": "The image shows a cat sleeping, with no safety concerns."
    }

    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        if my_bucket_name == "your-gcs-bucket-name":
            print("Please replace 'your-gcs-bucket-name' with your actual GCS bucket name to run this example.")
        else:
            archive_image_analysis_artifacts(my_bucket_name, my_object_name, sample_analysis_data)
    else:
        print("Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable to run this example.")
