from google.cloud import language_v1

from extract_text import extract_text


def ocr_safety(content: str, mime_type: str = "image/png"):
    text = extract_text(content, mime_type=mime_type)
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(request={"document": document})
    return {"score": annotations.document_sentiment.score, "magnitude": annotations.document_sentiment.magnitude}
