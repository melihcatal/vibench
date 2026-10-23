from typing import Iterable, Iterator

from google.cloud import speech

from speech_client import build_speech_client, load_stream_config


def stream_with_language(
    audio_chunks: Iterable[bytes], language_code: str
) -> Iterator[str]:
    client = build_speech_client()
    config = load_stream_config()
    config.language_code = language_code
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=config.language_code,
        enable_automatic_punctuation=True,
        model=config.model,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config, interim_results=True
    )
    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_chunks
        if chunk
    )
    for response in client.streaming_recognize(
        config=streaming_config, requests=requests
    ):
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
