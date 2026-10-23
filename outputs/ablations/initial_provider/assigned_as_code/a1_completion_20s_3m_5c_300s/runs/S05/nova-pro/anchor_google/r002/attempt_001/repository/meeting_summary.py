from google.cloud import language

def meeting_summary(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document)
    return response.document_sentiment.score
