from speech_client import get_speech_client


def save_audio_to_gcs(
    audio_content: bytes, bucket_name: str, destination_blob_name: str
) -> str:
    client = get_speech_client().storage_client
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(
        audio_content, content_type="audio/mpeg"
    )  # Assuming MP3 for now

    return f"gs://{bucket_name}/{destination_blob_name}"
