from google.cloud import language


def embed_text(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={
        "document": document
    })
    sentiment = response.document_sentiment.score
    return sentiment