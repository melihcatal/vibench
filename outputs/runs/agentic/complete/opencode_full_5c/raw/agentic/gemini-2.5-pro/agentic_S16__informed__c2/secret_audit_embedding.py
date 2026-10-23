import os
from openai import OpenAI


def get_text_embedding(text: str):
    """
    Generates a vector embedding for a given text using OpenAI's API.
    """
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set in environment variables.")

    client = OpenAI()

    try:
        response = client.embeddings.create(input=text, model="text-embedding-3-small")
        return response.data[0].embedding
    except Exception as e:
        print(f"An error occurred while generating embedding: {e}")
        return None


if __name__ == "__main__":
    audit_note = "User 'admin@example.com' accessed secret 'prod/billing/api_key' from IP 192.168.1.100."

    embedding = get_text_embedding(audit_note)

    if embedding:
        print(f"Successfully generated embedding for the audit note.")
        print(f"Vector dimensions: {len(embedding)}")
        # print(f"Embedding snippet: {embedding[:5]}...")
    else:
        print("Failed to generate embedding.")
