from typing import AsyncIterable, AsyncIterator

from google.cloud import speech_v1p1beta1 as speech

from speech_client import load_speech_config, make_client


async def stream_with_language(source: AsyncIterable[bytes], language_code: str = "en-US", enable_punctuation: bool = True) -> AsyncIterator[str]:
    cfg = load_speech_config()
    cfg.language_code = language_code
    cfg.enable_punctuation = enable_punctuation
    client = make_client()
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=cfg.language_code,
        enable_automatic_punctuation=cfg.enable_punctuation,
        model=cfg.model,
    )
    streaming_config = speech.StreamingRecognitionConfig(config=recognition_config, interim_results=True)
    requests = [speech.StreamingRecognizeRequest(streaming_config=streaming_config)]
    async for chunk in source:
        requests.append(speech.StreamingRecognizeRequest(audio_content=chunk))
    for response in client.streaming_recognize(requests=requests):
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
