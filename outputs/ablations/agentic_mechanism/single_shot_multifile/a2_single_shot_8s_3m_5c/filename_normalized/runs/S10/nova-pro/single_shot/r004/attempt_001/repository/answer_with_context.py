import os
from [HELPER] model_client import get_llm_client

client = get_llm_client()

def answer_with_context(question, context):
    response = client.completions.create(
        model="text-davinci-003",
        prompt=f"Answer the following question using the provided context: {question} Context: {context}",
        max_tokens=150
    )
    return response.choices[0].text.strip()
