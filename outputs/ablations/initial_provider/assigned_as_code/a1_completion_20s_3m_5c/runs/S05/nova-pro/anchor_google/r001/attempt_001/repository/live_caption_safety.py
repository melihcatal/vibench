from google.cloud import language
from google.cloud.language import enums

def check_safety(text):
    client = language.LanguageServiceClient()
    document = language.types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(document=document)
    sentiment = analysis.document_sentiment.score
    return sentiment > -0.5