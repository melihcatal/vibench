from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig


def stream_with_language(language_code: str = "en-US", enable_punctuation: bool = True):
    client = get_speech_client()
    config = StreamingRecognitionConfig(
        config=types.RecognitionConfig(
            encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=enable_punctuation,
            model="latest_long",
        ),
        interim_results=True,
    )

    def request_generator(audio_generator):
        for chunk in audio_generator:
            yield types.StreamingRecognizeRequest(audio_content=chunk)

    def response_generator(audio_generator):
        requests = request_generator(audio_generator)
        responses = client.streaming_recognize(config, requests)
        for response in responses:
            for result in response.results:
                yield {
                    "transcript": result.alternatives[0].transcript,
                    "is_final": result.is_final,
                    "stability": result.stability,
                }

    return response_generator
