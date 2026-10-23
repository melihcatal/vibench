from google.cloud import translate_v2 as translate
from typing import AsyncGenerator, Dict, Any


def translate_live_captions(
    transcript_chunks: AsyncGenerator[Dict[str, Any], None],
    target_language: str = "es",
) -> AsyncGenerator[Dict[str, Any], None]:
    """Translates live captions into another language using Google Cloud Translation."""
    client = translate.Client()

    async for chunk in transcript_chunks:
        if chunk["is_final"]:
            translation = client.translate(
                chunk["text"],
                target_language=target_language,
                source_language=chunk.get("language_code", "en"),
            )
            yield {
                "original_text": chunk["text"],
                "translated_text": translation["translatedText"],
                "target_language": target_language,
                "is_final": True,
            }
        else:
            yield {
                "original_text": chunk["text"],
                "translated_text": "",
                "target_language": target_language,
                "is_final": False,
            }
