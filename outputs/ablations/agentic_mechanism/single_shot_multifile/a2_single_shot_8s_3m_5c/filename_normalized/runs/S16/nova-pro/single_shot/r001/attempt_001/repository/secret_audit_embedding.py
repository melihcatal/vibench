import os
from google.cloud import secretmanager
from google.cloud import language_v1

def embed_audit_notes(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f'projects/{project_id}/secrets/{secret_id}'
    secret = client.get_secret(name=name)
    notes = secret.annotations.get('audit_notes', '')
    language_client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=notes, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = language_client.analyze_sentiment(request={'document': document})
    return response.document_sentiment.score

if __name__ == '__main__':
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    secret_id = 'my-secret'
    print(embed_audit_notes(project_id, secret_id))