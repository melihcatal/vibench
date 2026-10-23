from google.cloud import language
from google.cloud.language import enums

def summarize_text(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    summary = client.analyze_sentiment(document).document_sentiment.text
    return summary