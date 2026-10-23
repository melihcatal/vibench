from google.cloud import storage


def save_audio(audio_bytes, bucket_name, destination_blob_name, content_type="audio/mpeg"):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(audio_bytes, content_type=content_type)

    return {"gcs_uri": f"gs://{bucket_name}/{destination_blob_name}"}