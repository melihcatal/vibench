import os
import sys
from typing import List

from openai import OpenAI


def load_texts() -> List[str]:
    if len(sys.argv) > 1:
        return sys.argv[1:]
    data = sys.stdin.read().splitlines()
    return [line for line in data if line.strip()]


def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    client = OpenAI(api_key=api_key)
    texts = load_texts()
    if not texts:
        raise RuntimeError("No texts provided")

    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    vectors = [item.embedding for item in response.data]

    for vector in vectors:
        print(" ".join(str(value) for value in vector))


if __name__ == "__main__":
    main()
