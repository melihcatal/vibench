from google.cloud import storage

def archive_image_assets(bucket_name: str, image_data: bytes, captions: str, image_filename: str, captions_filename: str):
    """
    Archives image-analysis artifacts and derived captions in Google Cloud Storage.

    Args:
        bucket_name (str): The name of the GCS bucket.
        image_data (bytes): The raw image data to archive.
        captions (str): The derived captions for the image.
        image_filename (str): The desired filename for the image in GCS.
        captions_filename (str): The desired filename for the captions in GCS.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Upload image data
    image_blob = bucket.blob(image_filename)
    image_blob.upload_from_string(image_data, content_type='image/jpeg') # Assuming JPEG, adjust as needed
    print(f"Image {image_filename} uploaded to {bucket_name}.")

    # Upload captions
    captions_blob = bucket.blob(captions_filename)
    captions_blob.upload_from_string(captions, content_type='text/plain')
    print(f"Captions {captions_filename} uploaded to {bucket_name}.")
