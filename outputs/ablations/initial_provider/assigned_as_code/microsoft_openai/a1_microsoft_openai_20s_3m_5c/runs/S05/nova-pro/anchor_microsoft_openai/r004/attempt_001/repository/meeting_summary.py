from google.cloud import language_v1 as language

def summarize_text(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    summary = client.analyze_entities(document).entities[0].name
    return summary