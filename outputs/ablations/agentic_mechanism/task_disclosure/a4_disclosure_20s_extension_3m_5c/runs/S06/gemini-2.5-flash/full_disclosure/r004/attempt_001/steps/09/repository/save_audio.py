from google.cloud import storage

def save_audio_output(audio_bytes: bytes, local_file_path: str = None, gcs_bucket_name: str = None, gcs_object_name: str = None, content_type: str = "audio/wav"):
    if local_file_path:
        with open(local_file_path, "wb") as f:
            f.write(audio_bytes)
    elif gcs_bucket_name and gcs_object_name:
        client = storage.Client()
        bucket = client.bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_object_name)
        blob.upload_from_string(audio_bytes, content_type=content_type)
    else:
        raise ValueError("Either local_file_path or gcs_bucket_name and gcs_object_name must be provided.")