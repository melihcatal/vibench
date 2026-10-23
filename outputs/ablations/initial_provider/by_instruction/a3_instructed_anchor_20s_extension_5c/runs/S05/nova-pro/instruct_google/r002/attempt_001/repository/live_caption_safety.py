from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Check live transcript text for unsafe content
def live_caption_safety(text):
    client = language.LanguageServiceClient()
    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(document=document)
    return analysis.document_sentiment.score < -0.2