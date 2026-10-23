from __future__ import annotations

from typing import Iterable, List

from deepl import DeepLClient

from speech_models import CaptionChunk

DEEPL_TARGET_DEFAULT = "ES"


def translate_live_captions(
    chunks: Iterable[CaptionChunk],
    auth_key: str,
    target_lang: str = DEEPL_TARGET_DEFAULT,
) -> List[str]:
    client = DeepLClient(auth_key)
    texts = [chunk.text for chunk in chunks]
    if not texts:
        return []
    result = client.translate_text(texts, target_lang=target_lang)
    if isinstance(result, list):
        return [item.text for item in result]
    return [result.text]
