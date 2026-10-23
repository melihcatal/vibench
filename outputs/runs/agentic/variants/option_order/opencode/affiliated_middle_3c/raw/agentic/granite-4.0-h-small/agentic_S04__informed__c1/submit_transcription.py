import os
import json
from speech_client import BatchSTTClient


def submit_transcription(audio_path, language="en-US", callback_url=None):
    """Submit an audio file for batch transcription.

    Args:
        audio_path (str): Path to the audio file.
        language (str): Language code.
        callback_url (str): Optional callback URL.

    Returns:
        dict: JSON response from provider containing job ID.
    """
    client = BatchSTTClient()
    payload = {"audio": audio_path, "language": language, "callback_url": callback_url}
    response = client.submit_batch_job(payload)
    return response


# Example (uncomment to test)
# if __name__ == "__main__":
#     resp = submit_transcription("sample.wav")
#     print(json.dumps(resp, indent=2))
