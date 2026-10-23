from google.cloud import speech_v1p1beta1 as speech
from typing import AsyncIterable, Dict, Any


def stream_with_language(
    audio_source: AsyncIterable[bytes],
    language_code: str = "en-US",
    enable_punctuation: bool = True,
    model: str = "latest_long",
) -> AsyncIterable[Dict[str, Any]]:
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

    async def request_stream():
        async for chunk in audio_source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(streaming_config, request_stream())

    async for response in responses:
        for result in response.results:
            yield {
                "is_final": result.is_final,
                "transcript": result.alternatives[0].transcript,
                "confidence": result.alternatives[0].confidence,
            }
