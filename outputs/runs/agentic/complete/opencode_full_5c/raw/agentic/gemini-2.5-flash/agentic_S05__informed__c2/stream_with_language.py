from google.cloud import speech_v1p1beta1 as speech
from typing import Iterable, Generator

from speech_client import get_speech_client
from speech_models import RecognitionConfig, StreamingRecognitionConfig

def start_streaming_recognizer(audio_source: Iterable[bytes], 
                               language_code: str = "en-US", 
                               enable_automatic_punctuation: bool = True,
                               sample_rate_hertz: int = 16000)
                               -> Generator[speech.StreamingRecognizeResponse, None, None]:
    """
    Starts a streaming recognizer with specified language and punctuation settings.
    Yields streaming recognition responses from Google Cloud Speech-to-Text.
    """
    client = get_speech_client()

    # Configure the streaming request with language and punctuation settings
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # Assuming LINEAR16 for generic audio
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
    )

    # The first request contains the streaming configuration. Subsequent requests contain audio content.
    def request_generator(audio_iter: Iterable[bytes]):
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        for chunk in audio_iter:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    # Provider-identifying signal: google.cloud.speech_v1p1beta1
    responses = client.streaming_recognize(request_generator(audio_source))
    return responses

