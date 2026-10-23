from typing import Iterator, Optional

import boto3

from speech_models import TranscriptChunk


def translate_live_captions(chunks: Iterator[TranscriptChunk], target_language_code: str, source_language_code: Optional[str] = None) -> Iterator[str]:
    client = boto3.client("translate")
    for chunk in chunks:
        if not chunk.text:
            continue
        response = client.translate_text(Text=chunk.text, SourceLanguageCode=source_language_code or (chunk.language_code or "en"), TargetLanguageCode=target_language_code)
        yield response["TranslatedText"]
