from google.cloud import language_v1 as language

from speech_models import ModerationRequest, normalize_transcript_text


def moderate_transcript(transcript):
    client = language.LanguageServiceClient()
    text = normalize_transcript_text(transcript)
    request = ModerationRequest(text=text)
    document = language.Document(content=request.text, type_=language.Document.Type.PLAIN_TEXT)
    return client.analyze_sentiment(document=document)
