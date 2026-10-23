from google.cloud import language_v1

def summarize_transcription_results(transcript):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=transcript, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document)
    summary = ' '.join([entity.name for entity in response.entities])
    return summary