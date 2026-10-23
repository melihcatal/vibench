from google.cloud import language
from google.cloud.language import enums

def embed_text(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=enums.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(document)
    return analysis.document_sentiment.score