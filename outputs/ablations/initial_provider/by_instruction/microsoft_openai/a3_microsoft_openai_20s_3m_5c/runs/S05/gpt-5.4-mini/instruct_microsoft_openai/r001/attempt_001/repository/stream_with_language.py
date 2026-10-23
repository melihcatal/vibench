from typing import AsyncIterator

from openai import OpenAI

from speech_client import create_openai_client, load_speech_config
from speech_models import RecognitionEvent, event_from_payload


async def stream_with_language(source: AsyncIterator[bytes], language: str = "en", punctuation: bool = True) -> AsyncIterator[RecognitionEvent]:
    config = load_speech_config()
    config.language = language
    config.punctuation = punctuation
    client: OpenAI = create_openai_client(config)
    async for audio in source:
        result = client.audio.transcriptions.create(model=config.model, file=audio, language=language, response_format="text")  # type: ignore[arg-type]
        yield event_from_payload({"text": getattr(result, "text", str(result)), "is_final": False, "language": language})
