from security_models import AuditNote
import os
from openai import AzureOpenAI
from typing import List

def embed_audit_notes(audit_notes: List[AuditNote], azure_openai_endpoint: str = None, azure_openai_key: str = None, embedding_model: str = "text-embedding-ada-002") -> List[dict]:
    if azure_openai_endpoint is None:
        azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    if azure_openai_key is None:
        azure_openai_key = os.environ.get("AZURE_OPENAI_API_KEY")

    if not azure_openai_endpoint or not azure_openai_key:
        raise ValueError("Azure OpenAI endpoint and API key must be provided or set in environment variables.")

    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version="2023-05-15"
    )

    embeddings_results = []
    for note in audit_notes:
        response = client.embeddings.create(input=note.text, model=embedding_model)
        embeddings_results.append({
            "audit_note_id": note.id,
            "text": note.text,
            "embedding": response.data[0].embedding
        })
    return embeddings_results
