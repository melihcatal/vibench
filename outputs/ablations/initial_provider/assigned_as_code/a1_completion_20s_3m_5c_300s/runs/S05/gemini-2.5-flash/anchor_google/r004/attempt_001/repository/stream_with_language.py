from typing import Iterator, Dict, Any
from speech_client import SpeechClient
from speech_models import RecognitionRequest, SpeechRecognitionResult

def stream_with_language(audio_chunks: Iterator[bytes], sample_rate_hz: int, language_code: str, enable_automatic_punctuation: bool = True) -> Iterator[SpeechRecognitionResult]:
    speech_client = SpeechClient()
    request = RecognitionRequest(
        audio_chunks=audio_chunks,
        sample_rate_hz=sample_rate_hz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation
    )

    for result_dict in speech_client.streaming_recognize(request):
        # Convert the dictionary result to our SpeechRecognitionResult dataclass
        yield SpeechRecognitionResult(
            text=result_dict.get("text", ""),
            is_final=result_dict.get("is_final", False),
            language_code=result_dict.get("language_code", language_code) # Use the provided language_code if not explicitly in result
        )
