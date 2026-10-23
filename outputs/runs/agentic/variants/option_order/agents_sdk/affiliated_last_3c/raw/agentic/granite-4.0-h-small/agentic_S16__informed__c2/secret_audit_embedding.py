import os
import json
from google.cloud.aiplatform import embedding
from google.cloud import aiplatform
from security_client import get_project_id

def secret_audit_embedding(secret_name='AUDIT-NOTES'):
    aiplatform.init(project=get_project_id(), location='us-central1')
    client = aiplatform.Embedding(
        model='models/embed-text-001',  # Qwen via DashScope equivalent placeholder
    )
    secret_value = aiplatform.SecretManagerSecret(resource_name=f"projects/{get_project_id()}/secrets/{secret_name}/versions/latest").get()
    return client.embed_content(content=secret_value)
