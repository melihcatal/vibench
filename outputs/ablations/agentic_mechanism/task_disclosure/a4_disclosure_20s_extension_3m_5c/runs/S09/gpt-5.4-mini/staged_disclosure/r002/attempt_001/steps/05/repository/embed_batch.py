import os
import sys
from typing import List

from openai import OpenAI


def read_texts() -> List[str]:
    if len(sys.argv) > 1:
        return sys.argv[1:]
    data = sys.stdin.read().splitlines()
    return [line for line in data if line.strip()]


def main() -> int:
    texts = read_texts()
    if not texts:
        return 1
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    for item in response.data:
        print(item.index, item.embedding)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
