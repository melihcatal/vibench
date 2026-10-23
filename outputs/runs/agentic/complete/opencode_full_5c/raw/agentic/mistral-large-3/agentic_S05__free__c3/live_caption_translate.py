from google.cloud import translate_v3beta1 as translate
from typing import AsyncIterable, Dict, Any


def translate_live_captions(
    transcript_stream: AsyncIterable[Dict[str, Any]],
    target_language: str = "es",
) -> AsyncIterable[Dict[str, Any]]:
    client = translate.TranslationServiceClient()
    parent = f"projects/{client.project}/locations/global"

    async for result in transcript_stream:
        if result["is_final"]:
            response = client.translate_text(
                parent=parent,
                contents=[result["transcript"]],
                mime_type="text/plain",
                target_language_code=target_language,
            )
            yield {
                "original": result["transcript"],
                "translated": response.translations[0].translated_text,
                "language": target_language,
            }
        else:
            yield {
                "original": result["transcript"],
                "translated": "",
                "language": target_language,
            }
