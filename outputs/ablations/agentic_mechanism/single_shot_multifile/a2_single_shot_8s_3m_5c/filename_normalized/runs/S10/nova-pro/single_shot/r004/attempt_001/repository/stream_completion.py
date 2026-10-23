import os
from [HELPER] model_client import get_llm_client

client = get_llm_client()

def stream_completion(prompt):
    response = client.completions.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        stream=True
    )
    for chunk in response:
        print(chunk.choices[0].text, end='', flush=True)
