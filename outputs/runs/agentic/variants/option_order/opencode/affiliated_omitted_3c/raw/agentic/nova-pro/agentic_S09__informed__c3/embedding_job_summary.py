import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_embedding_job(job_id):
    response = client.embeddings.retrieve(job_id)
    return response.summary
