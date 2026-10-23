import os
from openai import OpenAI


def crypto_audit_embedding(text: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    return (
        client.embeddings.create(model="text-embedding-3-small", input=text)
        .data[0]
        .embedding
    )


if __name__ == "__main__":
    crypto_audit_embedding(os.environ.get("TEXT", ""))
