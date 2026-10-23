from google.cloud import texttospeech_v1 as texttospeech
import os


class AudioSaver:
    def __init__(self):
        pass

    def save_audio(self, audio_content: bytes, output_path: str) -> None:
        with open(output_path, "wb") as out:
            out.write(audio_content)

    def save_audio_to_object(
        self, audio_content: bytes, bucket_name: str, object_name: str
    ) -> None:
        from google.cloud import storage

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        blob.upload_from_string(audio_content)
