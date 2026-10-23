from typing import AsyncIterator, Optional

from google.cloud.speech_v2.types import cloud_speech

from speech_client import get_recognizer_path, get_speech_client
from speech_models import TranscriptChunk, normalize_transcript_text


async def stream_audio_chunks(
    chunks: AsyncIterator[bytes],
    language_code: str = "en-US",
    recognizer: Optional[str] = None,
) -> AsyncIterator[TranscriptChunk]:
    client = get_speech_client()
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[language_code],
        model="chirp_3",
    )

    async def requests() -> AsyncIterator[cloud_speech.StreamingRecognizeRequest]:
        yield cloud_speech.StreamingRecognizeRequest(
            recognizer=get_recognizer_path(recognizer=recognizer),
            streaming_config=cloud_speech.StreamingRecognitionConfig(
                config=config,
                streaming_features=cloud_speech.StreamingRecognitionFeatures(
                    interim_results=True
                ),
            ),
        )
        async for chunk in chunks:
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    stream = await client.streaming_recognize(requests=requests())
    async for response in stream:
        for result in response.results:
            if result.alternatives:
                yield TranscriptChunk(
                    text=normalize_transcript_text(result.alternatives[0].transcript),
                    is_final=result.is_final,
                    stability=getattr(result, "stability", None),
                    language_code=language_code,
                )
