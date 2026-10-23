import os
from typing import Iterable, List

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

from speech_models import TranscriptEvent, normalize_transcript_text


def translate_live_captions(
    chunks: Iterable[TranscriptEvent], target_language: str
) -> List[str]:
    client = TextTranslationClient(
        endpoint=os.environ["AZURE_TRANSLATOR_ENDPOINT"],
        credential=AzureKeyCredential(os.environ["AZURE_TRANSLATOR_KEY"]),
    )
    texts = [
        normalize_transcript_text(chunk.text)
        for chunk in chunks
        if normalize_transcript_text(chunk.text)
    ]
    if not texts:
        return []
    response = client.translate(content=texts, to=[target_language])
    return [item.translations[0].text for item in response]
