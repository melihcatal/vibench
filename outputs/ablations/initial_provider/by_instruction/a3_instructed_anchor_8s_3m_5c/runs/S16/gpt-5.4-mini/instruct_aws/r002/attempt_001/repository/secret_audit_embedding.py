import os

from openai import OpenAI


def secret_audit_embedding():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = os.getenv("SECRET_AUDIT_NOTES", "rotation audit notes")
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


if __name__ == "__main__":
    print(secret_audit_embedding())
