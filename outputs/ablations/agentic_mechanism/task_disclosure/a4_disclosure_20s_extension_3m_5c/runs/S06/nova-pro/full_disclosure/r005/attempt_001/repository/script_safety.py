from google.cloud import language_v2

def check_unsafe_content(text):
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(content=text, type_=language_v2.Document.Type.PLAIN_TEXT)
    response = client.analyze_entity_sentiment(request={'document': document})
    for entity in response.entities:
        if entity.salience > 0.5 and entity.sentiment.score < -0.5:
            return True
    return False