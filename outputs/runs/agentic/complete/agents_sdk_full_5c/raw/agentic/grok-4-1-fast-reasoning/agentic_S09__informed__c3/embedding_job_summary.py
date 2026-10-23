import os
from mistralai import MistralClient
from typing import dict, Any

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL = "open-mistral-nemo"

client = MistralClient(api_key=MISTRAL_API_KEY)

def embedding_job_summary(job_results: dict[str, Any]) -> str:
    prompt = f"""Provide a concise summary of the embedding job results:

{job_results}"""
    response = client.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content