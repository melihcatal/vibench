import os
from google.cloud import storage


def save_audio(audio_content: bytes, bucket_name: str, destination_blob_name: str):
    """
    Saves the synthesized audio content to a local file or a GCS bucket.

    Args:
        audio_content (bytes): The audio data to save.
        bucket_name (str): The name of the GCS bucket.
        destination_blob_name (str): The name of the blob to create.
    """
    # For local saving:
    # with open(destination_blob_name, "wb") as out:
    #     out.write(audio_content)
    # print(f'Audio content written to file "{destination_blob_name}"')

    # For GCS saving:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(audio_content)

    print(f"Audio content uploaded to gs://{bucket_name}/{destination_blob_name}")


def save_audio_local(audio_content: bytes, file_path: str):
    """
    Saves the synthesized audio content to a local file.
    Args:
        audio_content (bytes): The audio data to save.
        file_path (str): The local path to save the file.
    """
    with open(file_path, "wb") as out:
        out.write(audio_content)
