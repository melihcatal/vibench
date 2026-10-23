import os
from speech_client import get_storage_client


def save_audio_to_file(audio_content: bytes, file_path: str) -> None:
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    with open(file_path, "wb") as file:
        file.write(audio_content)


def save_audio_to_object(
    audio_content: bytes,
    bucket_name: str,
    object_name: str,
    content_type: str = "audio/mpeg",
) -> str:
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_string(audio_content, content_type=content_type)
    blob.make_public()
    return blob.public_url
