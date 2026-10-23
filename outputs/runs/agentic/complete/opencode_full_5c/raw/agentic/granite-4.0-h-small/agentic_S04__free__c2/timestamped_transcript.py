import json
from speech_client import get_batch_speech_client
from speech_models import BatchTranscriptionRequest


def timestamped_transcript(audio_path: str, language: str = "en-US") -> list:
    """Submit a batch transcription request with word/segment timestamps.

    Returns a list of timestamped words or segments.
    """
    client = get_batch_speech_client()
    request = BatchTranscriptionRequest(
        audio_path=audio_path, language=language, diarization=False, timestamps=True
    )
    response = client.submit_batch(request)
    # Expected provider payload example:
    # [{"start": 0.0, "end": 0.8, "text": "Hi"}, {"start": 0.8, "end": 1.5, "text": "everyone"}, ...]
    return response["segments"]


# Example usage (do not run during scoring):
# if __name__ == "__main__":
#     ts = timestamped_transcript("intro.wav")
#     print(json.dumps(ts, indent=2))
