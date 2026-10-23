import google.cloud.language


def embed_script(script):
    client = google.cloud.language.LanguageServiceClient()
    document = google.cloud.language.types.Document(content=script, type=google.cloud.language.enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    return response.document_sentiment.score