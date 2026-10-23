from typing import AsyncIterator, Optional

from google.cloud.speech_v2.types import cloud_speech

from speech_client import get_recognizer_path, get_speech_client


async def start_streaming_recognizer(
    audio_source: AsyncIterator[bytes],
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    recognizer: Optional[str] = None,
):
    client = get_speech_client()
    recognition_config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[language_code],
        model="latest_long",
        features=cloud_speech.RecognitionFeatures(
            enable_automatic_punctuation=enable_automatic_punctuation
        ),
    )

    async def requests() -> AsyncIterator[cloud_speech.StreamingRecognizeRequest]:
        yield cloud_speech.StreamingRecognizeRequest(
            recognizer=get_recognizer_path(recognizer=recognizer),
            streaming_config=cloud_speech.StreamingRecognitionConfig(
                config=recognition_config,
                streaming_features=cloud_speech.StreamingRecognitionFeatures(
                    interim_results=True
                ),
            ),
        )
        async for chunk in audio_source:
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    return await client.streaming_recognize(requests=requests())
