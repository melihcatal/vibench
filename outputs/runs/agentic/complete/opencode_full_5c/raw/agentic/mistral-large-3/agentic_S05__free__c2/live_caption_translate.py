from google.cloud import translate_v2 as translate
from typing import AsyncGenerator, Dict, Any


async def live_caption_translate(
    transcript_stream: AsyncGenerator[Dict[str, Any], None],
    target_language: str = "es",
) -> AsyncGenerator[Dict[str, Any], None]:
    client = translate.Client()

    async for event in transcript_stream:
        if event["is_final"]:
            translated = client.translate(
                event["transcript"], target_language=target_language
            )
            yield {
                "original": event["transcript"],
                "translated": translated["translatedText"],
                "language": target_language,
            }
        else:
            yield {
                "original": event["transcript"],
                "translated": "",
                "language": target_language,
            }
