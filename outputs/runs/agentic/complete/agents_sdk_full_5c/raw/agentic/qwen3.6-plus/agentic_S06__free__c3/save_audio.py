"""
save_audio.py - Writes synthesized speech audio to a local file or cloud object using Google Cloud Storage.

Supports saving audio bytes to local filesystem paths and uploading to
Google Cloud Storage buckets. Uses the google-cloud-storage SDK for
cloud object storage integration.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Union

from google.cloud import storage

from speech_models import SynthesisResponse


def _infer_filename_extension(response: SynthesisResponse) -> str:
    """Infer file extension from audio encoding in the synthesis response."""
    extension_map = {
        "LINEAR16": ".wav",
        "MP3": ".mp3",
        "OGG_OPUS": ".ogg",
        "MULAW": ".au",
    }
    return extension_map.get(response.encoding.value, ".mp3")


def save_audio_to_file(
    response: SynthesisResponse,
    output_path: Union[str, Path],
    overwrite: bool = False,
) -> Path:
    """
    Save synthesized audio bytes to a local file.

    Args:
        response: SynthesisResponse containing audio_content bytes.
        output_path: Destination file path. If directory, auto-appends filename.
        overwrite: If False and file exists, raises FileExistsError.

    Returns:
        Path to the written file.

    Raises:
        FileExistsError: If file exists and overwrite=False.
        IOError: On write failure.
    """
    output = Path(output_path)

    if output.is_dir():
        ext = _infer_filename_extension(response)
        output = output / f"tts_output{ext}"

    if output.exists() and not overwrite:
        raise FileExistsError(f"Output file already exists: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(response.audio_content)

    return output


def save_audio_to_gcs(
    response: SynthesisResponse,
    bucket_name: str,
    blob_name: Optional[str] = None,
    project_id: Optional[str] = None,
    credentials_path: Optional[str] = None,
    public_read: bool = False,
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> str:
    """
    Upload synthesized audio to a Google Cloud Storage bucket.

    Provider: Google Cloud Storage via google-cloud-storage SDK.
    API endpoint: storage.googleapis.com

    Args:
        response: SynthesisResponse containing audio_content bytes.
        bucket_name: GCS bucket name (e.g. "my-tts-audio-bucket").
        blob_name: Object name in the bucket. Auto-generated if None.
        project_id: Google Cloud project ID. Falls back to GOOGLE_CLOUD_PROJECT env.
        credentials_path: Path to Google service account JSON file.
        public_read: If True, grant allUsers read access to the blob.
        content_type: MIME type for the blob. Auto-detected from encoding if None.
        metadata: Optional custom metadata key-value pairs for the blob.

    Returns:
        GCS URI of the uploaded blob (gs://bucket_name/blob_name).

    Raises:
        google.api_core.exceptions.GoogleAPIError: On GCS upload failure.
        ValueError: If bucket_name is invalid.
    """
    if not bucket_name:
        raise ValueError("bucket_name is required.")

    if not blob_name:
        ext = _infer_filename_extension(response)
        import uuid

        blob_name = f"tts-synthesis/{uuid.uuid4().hex}{ext}"

    ct_map = {
        "LINEAR16": "audio/x-wav",
        "MP3": "audio/mpeg",
        "OGG_OPUS": "audio/ogg",
        "MULAW": "audio/basic",
    }
    detected_ct = ct_map.get(response.encoding.value, "audio/mpeg")
    content_type = content_type or detected_ct

    client_kwargs = {}
    if project_id:
        client_kwargs["project"] = project_id

    if credentials_path:
        from google.oauth2 import service_account

        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client_kwargs["credentials"] = credentials

    storage_client = storage.Client(**client_kwargs)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_string(
        response.audio_content,
        content_type=content_type,
    )

    if metadata:
        blob.metadata = metadata
        blob.patch()

    if public_read:
        blob.make_public()

    gcs_uri = f"gs://{bucket_name}/{blob_name}"
    return gcs_uri


def save_audio(
    response: SynthesisResponse,
    destination: Union[str, Path],
    overwrite: bool = False,
    project_id: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> str:
    """
    Save synthesized audio to local file or GCS based on destination format.

    If destination starts with 'gs://', uploads to Google Cloud Storage.
    Otherwise, saves to the local filesystem.

    Provider: Google Cloud Storage (google-cloud-storage SDK) for cloud paths.

    Args:
        response: SynthesisResponse with audio data.
        destination: Local file path or GCS URI (gs://bucket/object).
        overwrite: Allow overwrite for local files.
        project_id: GCS project ID (used for cloud destinations).
        credentials_path: GCS credentials path (used for cloud destinations).

    Returns:
        Path or GCS URI string where audio was saved.
    """
    dest_str = str(destination)

    if dest_str.startswith("gs://"):
        import re

        match = re.match(r"gs://([^/]+)/(.+)", dest_str)
        if not match:
            raise ValueError(f"Invalid GCS URI: {dest_str}")

        bucket_name = match.group(1)
        blob_name = match.group(2)

        return save_audio_to_gcs(
            response=response,
            bucket_name=bucket_name,
            blob_name=blob_name,
            project_id=project_id,
            credentials_path=credentials_path,
        )
    else:
        local_path = save_audio_to_file(response, destination, overwrite=overwrite)
        return str(local_path)


if __name__ == "__main__":
    from synthesize_text import synthesize_text

    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    result = synthesize_text(
        text="This audio was saved using Google Cloud Text-to-Speech.",
        language_code="en-US",
        voice_name="en-US-Wavenet-D",
        credentials_path=creds,
    )

    local_path = save_audio_to_file(result, Path("./output/speech.mp3"), overwrite=True)
    print(f"Saved audio to: {local_path}")
