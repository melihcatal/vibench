import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_embedding_job(job_id):
    response = client.completions.create(
        model="text-davinci-003",
        prompt=f"Summarize the embedding job with ID {job_id}",
        max_tokens=150,
    )
    return response.choices[0].text.strip()
