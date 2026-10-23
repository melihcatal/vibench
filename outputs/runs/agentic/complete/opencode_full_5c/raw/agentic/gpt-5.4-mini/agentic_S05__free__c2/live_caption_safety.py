from typing import Iterable, List

from google.cloud import language_v1

from speech_models import normalize_chunks


def check_caption_safety(chunks: Iterable[str]) -> List[str]:
    client = language_v1.LanguageServiceClient()
    findings: List[str] = []
    for chunk in normalize_chunks(chunks):
        document = language_v1.Document(
            content=chunk, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        response = client.analyze_sentiment(request={"document": document})
        if response.document_sentiment.score < -0.5:
            findings.append(chunk)
    return findings
