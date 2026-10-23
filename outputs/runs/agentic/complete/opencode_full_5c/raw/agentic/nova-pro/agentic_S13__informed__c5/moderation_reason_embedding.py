import os
import openai

# Set up the OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")


def moderation_reason_embedding(text):
    response = openai.Embedding.create(input=text, engine="text-similarity-davinci-001")
    return response["data"][0]["embedding"]
