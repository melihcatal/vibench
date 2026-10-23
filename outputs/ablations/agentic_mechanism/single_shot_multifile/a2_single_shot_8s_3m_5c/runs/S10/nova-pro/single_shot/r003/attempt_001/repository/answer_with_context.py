import os
from model_client import get_hosted_llm_client

client = get_hosted_llm_client()

def answer_with_context(question, context):
    response = client.answer_with_context(question, context)
    return response['answer']