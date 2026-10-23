import json
import os
from pathlib import Path
from typing import List

# Placeholder for cloud object storage client (e.g., AWS S3, GCS, Azure Blob)
# In production you would configure a concrete client with proper credentials


class StorageClient:
    def __init__(self, bucket_name: str, folder_prefix: str = "vision-assets"):
        self.bucket = bucket_name
        self.prefix = folder_prefix
        # Example: self.client = boto3.client('s3')
        # For demo purposes we just print upload actions

    def upload_file(self, local_path: str, remote_key: str):
        # Simulate upload - in real code you would call S3 client.put_object or similar
        print(
            f"[STORAGE] Uploading {local_path} to {self.bucket}/{self.prefix}/{remote_key}"
        )
        # Actual upload: self.client.upload_file(local_path, f"{self.prefix}/{remote_key}")

    def archive_artifact(self, artifact_path: str, key: str):
        self.upload_file(artifact_path, key)

    def archive_all(self, image_path: str, label_file: str, description_file: str):
        # Create a consistent naming scheme using the image filename
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        label_key = f"{self.prefix}/{base_name}_labels.json"
        desc_key = f"{self.prefix}/{base_name}_description.txt"
        text_key = f"{self.prefix}/{base_name}_text.txt"

        # Assume label_file/description_file/etc. are already written locally
        self.archive_artifact(label_file, label_key)
        self.archive_artifact(description_file, desc_key)
        self.archive_artifact(
            text_key, "."
        )  # placeholder - text may be generated later
        print("[STORAGE] Artifact archiving complete")


if __name__ == "__main__":
    # Example usage with dummy file paths - replace with real output files from pipeline
    storage = StorageClient(bucket_name="my-vision-assets")
    image_file = "example.jpg"
    label_path = "labels.json"
    desc_path = "description.txt"
    storage.archive_all(
        image_path=image_file, label_file=label_path, description_file=desc_path
    )
# Integration tip: call `archive_all` after all same-scenario steps finish successfully
