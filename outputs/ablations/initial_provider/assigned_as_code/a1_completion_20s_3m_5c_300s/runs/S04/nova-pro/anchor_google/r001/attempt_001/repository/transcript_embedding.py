from google.cloud import language

def transcript_embedding(transcript):
    client = language.LanguageServiceClient()
    document = language.Document(content=transcript, type_=language.Document.Type.PLAIN_TEXT)
    embedding = client.analyze_entity_sentiment(document=document)
    return embedding.document_sentiment.score