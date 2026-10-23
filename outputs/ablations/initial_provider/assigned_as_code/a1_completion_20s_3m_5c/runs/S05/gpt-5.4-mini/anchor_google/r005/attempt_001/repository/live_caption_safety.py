from google.cloud import language_v1

from speech_models import normalize_text


def live_caption_safety(payload, config=None):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=normalize_text(payload["text"]), type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document, "encoding_type": language_v1.EncodingType.UTF8})
    score = response.document_sentiment.score if response.document_sentiment else 0.0
    return {"text": normalize_text(payload["text"]), "unsafe": score < -0.5, "score": score}
