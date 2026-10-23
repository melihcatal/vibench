from openai import OpenAI

import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def crypto_audit_embedding(audit_note):
    response = client.embeddings.create(
        input=audit_note, model="text-embedding-ada-002"
    )
    return response.data[0].embedding
