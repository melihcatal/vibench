from openai import OpenAI


client = OpenAI()


def main(texts: list[str] | None = None) -> list:
    texts = texts or []
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in response.data]


if __name__ == "__main__":
    main()
