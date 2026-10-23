from google.cloud import language
from google.cloud.language import enums

def check_safety(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=enums.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(document=document)
    if analysis.document_sentiment.score < -0.2:
        return 'Unsafe'
    return 'Safe'