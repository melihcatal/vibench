import os
from [HELPER] model_client import get_llm_client

client = get_llm_client()

def summarize_text(text):
    response = client.completions.create(
        model="text-davinci-003",
        prompt=f"Summarize the following text: {text}",
        max_tokens=100
    )
    return response.choices[0].text.strip()
