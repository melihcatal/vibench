import os
from openai import OpenAI

def crypto_audit_embedding(text: str) -> list[float]:
    client = OpenAI()
    response = client.embeddings.create(model='text-embedding-3-large', input=text)
    return response.data[0].embedding

if __name__ == '__main__':
    print(crypto_audit_embedding(os.getenv('NOTE', '')))
