import os
import wave


def write_audio_to_file(
    audio_bytes: bytes, file_path: str, format: str = "wav"
) -> None:
    """Save raw audio bytes to a local file.

    Args:
        audio_bytes (bytes): Raw audio data.
        file_path (str): Destination path.
        format (str): Audio format ('wav', 'pcm', ...). Default is 'wav'.

    Raises:
        ValueError: If unsupported format is requested.
    """
    if format.lower() == "wav":
        with wave.open(file_path, "wb") as wf:
            # Assume 16-bit signed PCM, 2 channels, 16 kHz
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(audio_bytes)
    elif format.lower() == "pcm":
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
    else:
        raise ValueError(f"Unsupported format: {format}")


def save_to_object_storage(
    audio_bytes: bytes, bucket: str, key: str, format: str = "wav"
) -> None:
    """Stub for saving audio to an object storage (e.g., S3, GCS).

    Args:
        audio_bytes (bytes): Audio payload.
        bucket (str): Bucket/container name.
        key (str): Object key/path.
        format (str): Audio format.

    Note:
        Implement using boto3, google-cloud-storage, or equivalent client library as needed.
    """
    # Placeholder - replace with actual SDK/client call
    print(
        f"{format.upper()} audio ({len(audio_bytes)} bytes) would be uploaded to {bucket}/{key}"
    )
