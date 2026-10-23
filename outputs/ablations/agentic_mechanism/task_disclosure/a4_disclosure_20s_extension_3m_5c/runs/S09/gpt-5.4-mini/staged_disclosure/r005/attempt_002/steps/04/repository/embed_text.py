import os
from openai import OpenAI


def embed_text(text: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


if __name__ == "__main__":
    import sys

    print(embed_text(sys.argv[1] if len(sys.argv) > 1 else ""))
