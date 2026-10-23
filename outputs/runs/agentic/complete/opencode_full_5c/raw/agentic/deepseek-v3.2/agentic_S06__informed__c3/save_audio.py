import os
import wave
import io


def save_audio_to_file(
    audio_data, filepath, sample_rate=16000, sample_width=2, channels=1
):
    with wave.open(filepath, "wb") as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data)

    return filepath


def save_audio_to_bytes(audio_data, sample_rate=16000, sample_width=2, channels=1):
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data)

    buffer.seek(0)
    return buffer.read()


def save_audio_to_s3(audio_data, bucket_name, object_key, s3_client=None):
    if s3_client is None:
        import boto3

        s3_client = boto3.client("s3")

    buffer = io.BytesIO(audio_data)
    s3_client.upload_fileobj(buffer, bucket_name, object_key)

    return f"s3://{bucket_name}/{object_key}"


def save_audio_to_azure_blob(
    audio_data, container_name, blob_name, blob_service_client=None
):
    if blob_service_client is None:
        from azure.storage.blob import BlobServiceClient

        connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
        if not connection_string:
            raise ValueError(
                "AZURE_STORAGE_CONNECTION_STRING environment variable must be set"
            )
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )
    blob_client.upload_blob(audio_data, overwrite=True)

    return blob_client.url


def get_audio_format_info(audio_data):
    try:
        buffer = io.BytesIO(audio_data)
        with wave.open(buffer, "rb") as wav_file:
            return {
                "channels": wav_file.getnchannels(),
                "sample_width": wav_file.getsampwidth(),
                "frame_rate": wav_file.getframerate(),
                "nframes": wav_file.getnframes(),
                "duration_seconds": wav_file.getnframes() / wav_file.getframerate(),
            }
    except:
        return {"size_bytes": len(audio_data), "format": "raw_pcm"}
