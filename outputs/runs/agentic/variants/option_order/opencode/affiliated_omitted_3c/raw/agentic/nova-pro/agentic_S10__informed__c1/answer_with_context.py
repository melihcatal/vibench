import os
from ibm_watsonx_ai import ModelClient

client = ModelClient(os.getenv("WATSONX_API_KEY"), os.getenv("WATSONX_PROJECT_ID"))


def answer_with_context(question, context):
    response = client.answer_with_context(question, context)
    return response
