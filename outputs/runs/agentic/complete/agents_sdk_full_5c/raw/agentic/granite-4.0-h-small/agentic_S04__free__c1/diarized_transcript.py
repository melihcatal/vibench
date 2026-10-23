import os
import json
from speech_client import BatchSpeechClient
from speech_models import SpeechToTextConfig

# ------------------------------------------------------------
# diarized_transcript.py
# Request speaker diarization for a recorded meeting using Azure Speech Service
# ------------------------------------------------------------

def diarized_transcription(audio_path: str, language: str = "en-US") -> dict:
    """Submit a meeting audio file for transcription with diarization.

    Returns the raw JSON response (including speaker IDs) from the service.
    """
    client = BatchSpeechClient()
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    response = client.submit_batch_transcription(
        audio_bytes=audio_bytes,
        content_type="audio/wav",
        language=language,
        diarization_enabled=True
    )
    return json.loads(response)

# Example (run as script)
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Submit meeting audio with diarization.")
    parser.add_argument("audio_path", help="Path to WAV audio file.")
    parser.add_argument("language", nargs='?', default="en-US", help="BCP-47 language tag.")
    args = parser.parse_args()
    result = diarized_transcription(args.audio_path, args.language)
    print(json.dumps(result, indent=2))
