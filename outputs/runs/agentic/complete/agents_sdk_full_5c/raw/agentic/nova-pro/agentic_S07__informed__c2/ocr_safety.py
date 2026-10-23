from google.cloud import language

def check_safety(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    return response.document_sentiment.score > -0.5