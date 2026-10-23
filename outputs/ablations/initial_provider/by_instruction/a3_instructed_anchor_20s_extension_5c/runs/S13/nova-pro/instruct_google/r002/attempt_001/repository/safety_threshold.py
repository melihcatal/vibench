from google.cloud import language_v1

def safety_threshold(text, threshold=-0.5):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    sentiment = response.document_sentiment
    return sentiment.score >= threshold