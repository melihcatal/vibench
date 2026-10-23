from openai import OpenAI


def embed_log_messages(messages: list[str]) -> list[list[float]]:
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-small", input=messages)
    return [item.embedding for item in response.data]


if __name__ == "__main__":
    embed_log_messages(["sample log message"])
