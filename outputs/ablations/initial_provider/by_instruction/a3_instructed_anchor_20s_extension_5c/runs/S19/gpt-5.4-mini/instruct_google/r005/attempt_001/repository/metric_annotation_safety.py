import re

from google.cloud import language_v1


def metric_annotation_safety(text: str):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document}).document_sentiment
    unsafe = bool(re.search(r"(?:passwd|secret|token|drop\s+table)", text, re.I)) or (sentiment.score < -0.5 and sentiment.magnitude > 0.5)
    return {"unsafe": unsafe, "score": sentiment.score, "magnitude": sentiment.magnitude}
