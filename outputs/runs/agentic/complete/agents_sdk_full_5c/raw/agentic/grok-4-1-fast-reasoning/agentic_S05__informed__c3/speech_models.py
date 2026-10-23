from dataclasses import dataclass
from google.cloud import speech

@dataclass
class SpeechResult:
    transcript: str
    is_final: bool

def get_streaming_config(
    language_code: str = "en-US",
    model: str = "short",
    enable_automatic_punctuation: bool = True,
    sample_rate_hertz: int = 16000,
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
):
    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        model=model,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    return speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )
