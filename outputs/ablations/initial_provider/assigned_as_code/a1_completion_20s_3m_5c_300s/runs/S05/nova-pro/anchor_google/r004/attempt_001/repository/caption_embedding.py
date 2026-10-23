from google.cloud import language


def embed_text(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type=language.Document.Type.PLAIN_TEXT)
    embedding = client.analyze_sentiment(document=document).document_sentiment.score
    return embedding