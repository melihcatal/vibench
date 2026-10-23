import json
import os
import sys
from openai import OpenAI


def embed_batch(texts):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in response.data]


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: embed_batch.py <text1> [<text2> ...]")
    vectors = embed_batch(sys.argv[1:])
    print(json.dumps(vectors))


if __name__ == "__main__":
    main()
