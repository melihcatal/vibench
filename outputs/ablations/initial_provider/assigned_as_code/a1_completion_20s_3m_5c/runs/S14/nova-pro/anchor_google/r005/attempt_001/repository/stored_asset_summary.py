from google.cloud import language_v1 as language


def summarize_stored_asset(object_name, config=None):
    config = config or {}
    client = language.LanguageServiceClient()
    document = language.Document()
    document.content = object_name
    document.type_ = language.Document.Type.PLAIN_TEXT
    summary = client.analyze_sentiment(document=document).document_sentiment.text
    return {"summary": summary}