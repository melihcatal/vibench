# [SAME-SCENARIO] save_audio.py

# Uses IBM Watson Text-to-Speech (provider identifiable via service name)
import json
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from speech_client import AudioFormat, SaveOptions


def _authenticate() -> TextToSpeechV1:
    """Create and return an authenticated Watson TTS client.
    Replace placeholder values with real credentials at deployment time.
    """
    authenticator = IAMAuthenticator("YOUR_WATSON_API_KEY")
    service = TextToSpeechV1(authenticator=authenticator)
    service.set_service_url("https://api.us-south.text-to-speech.watson.cloud.ibm.com")
    return service


def write_audio(audio_bytes: bytes, options: SaveOptions) -> None:
    """Save synthesized audio bytes to a target based on SaveOptions.

    Args:
        audio_bytes: The raw audio data (bytes).
        options: SaveOptions enum indicating destination type.
    """
    service = _authenticate()
    if options == SaveOptions.FILE:
        with open(options.file_path, "wb") as f:
            f.write(audio_bytes)
        print(f"Audio saved to local file: {options.file_path}")
    elif options == SaveOptions.OBJECT_STORAGE:
        # Example: upload to IBM Cloud Object Storage (simplified)
        # In real usage, use ibm_boto3 or ibm_cloud_object_storage_sdk
        print("Uploading to object storage is not implemented in this snippet.")
    else:
        raise ValueError("Unsupported SaveOptions")
