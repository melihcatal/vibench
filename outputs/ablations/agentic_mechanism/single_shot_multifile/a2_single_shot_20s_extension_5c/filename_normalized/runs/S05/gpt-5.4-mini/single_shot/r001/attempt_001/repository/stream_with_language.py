from typing import AsyncIterator, Dict

from google.cloud import speech
from google.cloud.speech import types as speech_types

from speech_client import get_speech_client, load_speech_config
from speech_models import normalize_stream_event


async def stream_with_language(audio_chunks: AsyncIterator[bytes], language_code: str, enable_punctuation: bool = True) -> AsyncIterator[Dict[str, object]]:
    config = load_speech_config()
    client = get_speech_client()
    recognizer_config = speech_types.RecognitionConfig(
        encoding=speech_types.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=config.sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
    )
    stream_config = speech_types.StreamingRecognitionConfig(config=recognizer_config, interim_results=True)

    async def request_iter():
        async for chunk in audio_chunks:
            yield speech_types.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(stream_config, request_iter())
    for response in responses:
        for result in response.results:
            if not result.alternatives:
                continue
            alt = result.alternatives[0]
            yield normalize_stream_event(
                transcript=alt.transcript,
                is_final=result.is_final,
                confidence=getattr(alt, 'confidence', None),
                language_code=language_code,
            )

