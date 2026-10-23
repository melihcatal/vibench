import openai


def embed_log_message(log_text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Embedding.create(input=log_text, model="text-embedding-ada-002")
    return response["data"][0]["embedding"]


if __name__ == "__main__":
    print(embed_log_message("This is a test log message."))
