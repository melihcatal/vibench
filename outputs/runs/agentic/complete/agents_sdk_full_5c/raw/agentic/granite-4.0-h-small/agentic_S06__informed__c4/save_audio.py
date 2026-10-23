import pathlib

AUDIO_DIR = pathlib.Path("audio")


def write_audio_to_file(audio_bytes, filename: str):
    """Write the raw audio bytes to a local .wav file in the ./audio folder."""
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    file_path = AUDIO_DIR / f"{filename}.wav"
    file_path.write_bytes(audio_bytes)
    return str(file_path)


def write_audio_to_object_store(audio_bytes, key: str):
    """Placeholder for uploading audio to an object storage bucket.
    In a real environment you would use the provider's SDK (e.g., AWS S3 boto3, GCS client, etc.).
    For illustration the function simply returns a simulated bucket URL.
    """
    return f"https://my-bucket.storage.googleapis.com/{key}.wav"

# Example usage (run as a script)
# if __name__ == "__main__":
#     raw_audio = b\"\"  # replace with real bytes from the TTS call
#     print(write_audio_to_file(raw_audio, "demo"))
#     print(write_audio_to_object_store(raw_audio, "demo-key"))
