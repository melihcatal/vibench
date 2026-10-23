
import openai
import os

def embed_text(text):
    """
    Embeds text using OpenAI's embedding API.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

if __name__ == "__main__":
    audit_note = "This is a crypto audit note about smart contract vulnerabilities."
    embedding = embed_text(audit_note)
    print(f"Embedding length: {len(embedding)}")
    print(f"First 5 embedding values: {embedding[:5]}")
