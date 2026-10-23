import json
from speech_client import get_batch_speech_client
from speech_models import BatchTranscriptionRequest


def diarized_transcript(audio_path: str, language: str = "en-US") -> list:
    """Submit a batch transcription request with speaker diarization.

    Returns a list of segments annotated with speaker labels.
    """
    client = get_batch_speech_client()
    request = BatchTranscriptionRequest(
        audio_path=audio_path, language=language, diarization=True, timestamps=False
    )
    response = client.submit_batch(request)
    # Assuming provider returns JSON like: [{"speaker": "A", "start": 1.2, "end": 4.5, "text": "Hello"}, ...]
    return response["segments"]


# Example invocation (commented out):
# if __name__ == "__main__":
#     segments = diarized_transcript("meeting.wav")
#     print(json.dumps(segments, indent=2))
