from google.cloud import language
from google.cloud.language import enums

def summarize_meeting(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document)
    return response.document_sentiment.text