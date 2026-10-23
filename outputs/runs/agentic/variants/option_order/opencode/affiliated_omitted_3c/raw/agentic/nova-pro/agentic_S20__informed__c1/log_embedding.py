import openai


def embed_log_message(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response["data"][0]["embedding"]


if __name__ == "__main__":
    text = "This is a sample log message."
    embedding = embed_log_message(text)
    print(embedding)
