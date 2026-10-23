from dataclasses import dataclass


@dataclass
class StreamingRecognitionRequest:
    audio_content: bytes


@dataclass
class StreamingRecognitionResponse:
    transcript: str
    is_final: bool


def normalize_google_response(response):
    if not response.results:
        return None

    result = response.results[0]
    if not result.alternatives:
        return None

    return StreamingRecognitionResponse(
        transcript=result.alternatives[0].transcript,
        is_final=result.is_final,
    )
