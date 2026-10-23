import os

from openai import OpenAI


def main() -> list[float]:
    client = OpenAI()
    text = os.getenv("LOG_TEXT", "")
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


if __name__ == "__main__":
    main()
