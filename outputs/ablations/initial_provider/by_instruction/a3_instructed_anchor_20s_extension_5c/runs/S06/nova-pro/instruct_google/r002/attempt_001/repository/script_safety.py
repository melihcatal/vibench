from google.cloud import language
from google.cloud.language import enums

def check_safety(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(document=document)
    return analysis.document_sentiment.score >= 0