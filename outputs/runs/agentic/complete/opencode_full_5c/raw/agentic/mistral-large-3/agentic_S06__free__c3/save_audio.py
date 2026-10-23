from google.cloud import texttospeech_v1 as tts
import os


class AudioSaver:
    def __init__(self, output_path: str):
        self.output_path = output_path

    def save_audio(self, audio_content: bytes, format: str = "wav") -> str:
        if not self.output_path.endswith(f".{format}"):
            self.output_path = f"{self.output_path}.{format}"

        with open(self.output_path, "wb") as out:
            out.write(audio_content)

        return self.output_path

    def save_to_object_storage(
        self, audio_content: bytes, bucket_name: str, object_name: str
    ) -> str:
        from google.cloud import storage

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        blob.upload_from_string(audio_content)
        return f"gs://{bucket_name}/{object_name}"
