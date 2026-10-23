from google.cloud import language_v1 as language

def check_safety(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(document=document)
    sentiment = analysis.document_sentiment.score
    if sentiment < -0.5:
        return 'Unsafe'
    else:
        return 'Safe'