from google.cloud import language

def moderate_transcript(transcript):
    client = language.LanguageServiceClient()
    document = language.Document(content=transcript, type_=language.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(document=document)
    if analysis.document_sentiment.score < 0:
        return "Moderation required"
    else:
        return "Moderation passed"