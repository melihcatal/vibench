import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def embed_log_message(log_text):
    response = openai.Embedding.create(input=log_text, model="text-embedding-ada-002")
    return response["data"][0]["embedding"]


if __name__ == "__main__":
    print(embed_log_message("Sample log message"))
