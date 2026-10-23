from google.cloud import speech_v1p1beta1 as speech
from typing import Optional, Generator, Dict, Any


def stream_with_language(
    language_code: str = "en-US",
    enable_punctuation: bool = True,
    model: str = "latest_long",
) -> Generator[Dict[str, Any], None, None]:
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
        model=model,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    def audio_generator():
        # Placeholder for actual audio generator
        yield b""

    requests = (
        speech.StreamingRecognizeRequest(audio_content=content)
        for content in audio_generator()
    )
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        for result in response.results:
            yield {
                "transcript": result.alternatives[0].transcript,
                "is_final": result.is_final,
                "stability": result.stability,
            }
