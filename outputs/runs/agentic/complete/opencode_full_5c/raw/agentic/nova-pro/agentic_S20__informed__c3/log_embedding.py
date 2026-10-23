import openai

openai.api_key = "YOUR_OPENAI_API_KEY"


def embed_log_message(log_message):
    response = openai.Embedding.create(
        input=log_message, model="text-embedding-ada-002"
    )
    return response["data"][0]["embedding"]
