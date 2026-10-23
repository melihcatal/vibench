from google.cloud import language


def summarize_text(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type=language.Document.Type.PLAIN_TEXT)
    summary = client.analyze_sentiment(document=document).document_sentiment.text
    return summary