import os
import sys
from openai import OpenAI


def embed_text(text: str):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: embed_text.py <text>")
    vector = embed_text(sys.argv[1])
    print(vector)


if __name__ == "__main__":
    main()
