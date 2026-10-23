import google.auth
from google.cloud import language_v1


def embed_script(script):
    credentials, project = google.auth.default()
    client = language_v1.LanguageServiceClient(credentials=credentials, project=project)
    document = language_v1.Document(content=script, type_=language_v1.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_entities(document=document)
    entities = [entity.name for entity in analysis.entities]
    return entities