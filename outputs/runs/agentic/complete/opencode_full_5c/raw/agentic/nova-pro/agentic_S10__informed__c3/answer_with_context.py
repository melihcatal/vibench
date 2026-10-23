import os
from mistralai.client import Client

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

client = Client(api_key=MISTRAL_API_KEY)


def answer_with_context(question, context):
    response = client.answer(question, context)
    return response.answer
