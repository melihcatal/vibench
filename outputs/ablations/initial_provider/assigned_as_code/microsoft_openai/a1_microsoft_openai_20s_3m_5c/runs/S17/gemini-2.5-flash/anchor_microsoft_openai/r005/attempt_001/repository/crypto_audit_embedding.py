import os
from openai import AzureOpenAI

def embed_audit_note(audit_note: str, azure_openai_endpoint: str, azure_openai_key: str, deployment_name: str) -> dict:
    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version="2024-02-01"
    )

    response = client.embeddings.create(
        input=audit_note,
        model=deployment_name # deployment_name is the model name in Azure OpenAI
    )

    embedding = response.data[0].embedding
    return {"audit_note": audit_note, "embedding": embedding}

# Example usage (requires AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME env vars)
# endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
# key = os.environ["AZURE_OPENAI_KEY"]
# deployment = os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"]
# note = "Audit log: Key rotation event for key_id: some_key_id on 2026-09-20."
# embedding_result = embed_audit_note(note, endpoint, key, deployment)
# print(embedding_result)
