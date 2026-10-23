
import os
from google.cloud import storage

def archive_asset_to_gcs(bucket_name: str, source_file_name: str, destination_blob_name: str):
    """Uploads a file to a Google Cloud Storage bucket."""
    # This example requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.")
    return blob.public_url # Or blob.name if you prefer the path within the bucket

def archive_text_to_gcs(bucket_name: str, text_content: str, destination_blob_name: str):
    """Uploads text content to a Google Cloud Storage bucket as a blob."""
    # This example requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(text_content)

    print(f"Text content uploaded to {destination_blob_name} in bucket {bucket_name}.")
    return blob.public_url

if __name__ == '__main__':
    # This example requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    # Replace with your bucket name and a dummy file/content for testing.
    # Ensure the bucket exists and your credentials have write access.
    test_bucket_name = os.environ.get("GCS_ARCHIVE_BUCKET", "your-gcs-archive-bucket")
    
    # Example 1: Archiving a dummy file
    dummy_file_name = "dummy_image_analysis_report.txt"
    with open(dummy_file_name, "w") as f:
        f.write("This is a dummy report of image analysis.\n")
        f.write("Labels: cat, animal\n")
        f.write("Description: A cat.")

    print("\nArchiving a dummy file...")
    file_blob_name = f"reports/{os.path.basename(dummy_file_name)}"
    try:
        file_public_url = archive_asset_to_gcs(test_bucket_name, dummy_file_name, file_blob_name)
        print(f"Archived file URL: {file_public_url}")
    except Exception as e:
        print(f"Error archiving file: {e}")
    finally:
        os.remove(dummy_file_name) # Clean up dummy file

    # Example 2: Archiving text content directly
    analysis_caption = "A detailed description of the image content: a fluffy white cat." # Example derived caption
    caption_blob_name = "captions/cat_description.txt"
    print("\nArchiving text content...")
    try:
        caption_public_url = archive_text_to_gcs(test_bucket_name, analysis_caption, caption_blob_name)
        print(f"Archived caption URL: {caption_public_url}")
    except Exception as e:
        print(f"Error archiving text content: {e}")
