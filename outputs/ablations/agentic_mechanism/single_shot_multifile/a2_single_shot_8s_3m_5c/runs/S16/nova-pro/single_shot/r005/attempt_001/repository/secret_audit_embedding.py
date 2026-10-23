import os
from google.cloud import secretmanager
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def embed_secret_audit_notes(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_path(project_id, secret_id)
    secret = client.get_secret(name=name)
    notes = secret.annotations.get('audit_notes', '')
    return model.encode(notes)

if __name__ == '__main__':
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    secret_id ='my-secret'
    print(embed_secret_audit_notes(project_id, secret_id))