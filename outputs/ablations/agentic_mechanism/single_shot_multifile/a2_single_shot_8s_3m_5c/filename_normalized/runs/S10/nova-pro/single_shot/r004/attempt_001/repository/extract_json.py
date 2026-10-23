import os
from [HELPER] model_client import get_llm_client

client = get_llm_client()

def extract_json(text):
    response = client.completions.create(
        model="text-davinci-003",
        prompt=f"Extract structured JSON from the following text: {text}",
        max_tokens=200
    )
    return response.choices[0].text.strip()
