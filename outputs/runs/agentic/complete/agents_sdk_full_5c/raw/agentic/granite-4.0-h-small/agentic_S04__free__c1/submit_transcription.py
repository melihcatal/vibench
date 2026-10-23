import os
import json
from speech_client import BatchSpeechClient
from speech_models import TranscriptionRequest, TranscriptionResponse

# ------------------------------------------------------------
# submit_transcription.py
# Submit an audio file for batch transcription using Azure Speech Service
# ------------------------------------------------------------

def submit_transcription(audio_path: str, language: str = "en-US") -> TranscriptionResponse:
    """Submit a WAV/PCM audio file for asynchronous batch transcription.

    Returns the parsed JSON response (TranscriptionResponse) containing the job ID.
    """
    client = BatchSpeechClient()  # uses AZURE_SPEECH_API_KEY env var
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    response = client.submit_batch_transcription(
        audio_bytes=audio_bytes,
        content_type="audio/wav",
        language=language
    )
    return TranscriptionResponse.parse_obj(response)

# Example (not executed in library code)
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Submit audio for batch transcription.")
    parser.add_argument("audio_path", help="Path to WAV audio file.")
    parser.add_argument("language", nargs='?', default="en-US", help="BCP-47 language tag.")
    args = parser.parse_args()
    result = submit_transcription(args.audio_path, args.language)
    print(json.dumps(result.dict(), indent=2))
