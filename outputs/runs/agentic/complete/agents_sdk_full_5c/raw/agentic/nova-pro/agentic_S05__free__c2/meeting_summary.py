from google.cloud import language_v1 as language

def summarize_meeting(text):
    client = language.LanguageServiceClient()
    document = language.types.Document(content=text, type_=language.enums.Document.Type.PLAIN_TEXT)
    summary = client.analyze_sentiment(document).document_sentiment.text
    return summary