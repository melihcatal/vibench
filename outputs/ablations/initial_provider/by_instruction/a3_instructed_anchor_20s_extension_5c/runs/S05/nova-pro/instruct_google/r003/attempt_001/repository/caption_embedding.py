import speech_client
import google.cloud.language

def caption_embedding(transcript):
    language_client = google.cloud.language.LanguageServiceClient()
    document = google.cloud.language.types.Document(content=transcript, type_=google.cloud.language.enums.Document.Type.PLAIN_TEXT)
    embedding = language_client.analyze_entity_sentiment(document).entities[0].salience
    return embedding