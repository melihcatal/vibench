from google.cloud import language
from google.cloud.language import enums


def meeting_summary(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    return response.document_sentiment.score