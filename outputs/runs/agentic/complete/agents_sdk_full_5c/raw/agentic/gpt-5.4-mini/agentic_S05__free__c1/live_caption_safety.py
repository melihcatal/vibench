from __future__ import annotations

from typing import Iterable, List

from google.cloud import language_v1

from speech_models import normalize_transcript


def check_caption_safety(captions: Iterable[str]) -> List[str]:
    client = language_v1.LanguageServiceClient()
    outputs: List[str] = []
    for caption in captions:
        text = normalize_transcript(caption)
        if not text:
            continue
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
        outputs.append("unsafe" if sentiment.score < -0.6 else "safe")
    return outputs
