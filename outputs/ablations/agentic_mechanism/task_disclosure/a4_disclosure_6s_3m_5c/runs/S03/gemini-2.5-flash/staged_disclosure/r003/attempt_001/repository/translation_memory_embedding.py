import os
from openai import OpenAI

def embed_text(text: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

if __name__ == "__main__":
    translated_segment = "Hello, world!"
    embedding = embed_text(translated_segment)
    print(f"Embedding for \"{translated_segment}\": {embedding[:5]}...") # Print first 5 elements for brevity
