from typing import Iterable, List

from google.cloud import language_v1 as language


def check_caption_safety(captions: Iterable[str]) -> List[float]:
    client = language.LanguageServiceClient()
    scores: List[float] = []
    for caption in captions:
        doc = language.Document(
            content=caption, type_=language.Document.Type.PLAIN_TEXT
        )
        result = client.analyze_sentiment(document=doc)
        scores.append(result.document_sentiment.score)
    return scores
