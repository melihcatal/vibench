import speech_client
import google.cloud.language

def live_caption_safety(transcript):
    language_client = google.cloud.language.LanguageServiceClient()
    document = google.cloud.language.types.Document(content=transcript, type_=google.cloud.language.enums.Document.Type.PLAIN_TEXT)
    analysis = language_client.analyze_sentiment(document)
    return analysis.document_sentiment.score >= 0.5