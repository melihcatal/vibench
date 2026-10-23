import os

from openai import OpenAI


def embed_log_message(message: str) -> list:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model="text-embedding-3-small", input=message)
    return response.data[0].embedding


def main() -> None:
    embed_log_message("payment timeout retry")


if __name__ == "__main__":
    main()
