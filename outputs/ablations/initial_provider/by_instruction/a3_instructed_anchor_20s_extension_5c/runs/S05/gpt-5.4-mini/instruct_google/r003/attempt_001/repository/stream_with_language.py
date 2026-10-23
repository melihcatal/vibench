from typing import Iterable

from google.cloud import speech_v1p1beta1 as speech

from speech_client import SpeechConfig, create_speech_client, create_recognition_config
from speech_models import normalize_text


def stream_with_language(audio_chunks: Iterable[bytes], language_code: str = "en-US", enable_punctuation: bool = True):
    client = create_speech_client()
    config = create_recognition_config(SpeechConfig(language_code=language_code, enable_punctuation=enable_punctuation))
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_chunks)
    for response in client.streaming_recognize(config=streaming_config, requests=requests):
        for result in response.results:
            if result.alternatives:
                yield normalize_text(result.alternatives[0].transcript)
