from google.cloud import language
from google.cloud.language import enums


def caption_embedding(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(request={"document": document})
    return response.entities