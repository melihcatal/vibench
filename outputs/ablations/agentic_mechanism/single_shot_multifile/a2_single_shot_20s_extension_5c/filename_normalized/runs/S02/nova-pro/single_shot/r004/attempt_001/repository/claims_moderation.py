from google.cloud import language_v1

def moderate_claims(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    sentiment = response.document_sentiment
    if sentiment.score < -0.5:
        return 'Moderated'
    else:
        return 'Approved'

if __name__ == '__main__':
    print(moderate_claims('your text here'))