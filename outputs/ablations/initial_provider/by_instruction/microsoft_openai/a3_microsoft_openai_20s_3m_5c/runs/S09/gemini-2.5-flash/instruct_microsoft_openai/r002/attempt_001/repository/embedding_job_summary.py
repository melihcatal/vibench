import os
import openai
from typing import List, Dict, Any

class EmbeddingJobResult:
    def __init__(self, job_id: str, texts_processed: int, status: str, errors: List[str] = None):
        self.job_id = job_id
        self.texts_processed = texts_processed
        self.status = status
        self.errors = errors if errors is not None else []

def summarize_embedding_job(job_result: EmbeddingJobResult) -> str:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"Summarize the embedding job with ID {job_result.job_id}. " \
             f"It processed {job_result.texts_processed} texts and its status is {job_result.status}. "
    if job_result.errors:
        prompt += f"There were errors: {', '.join(job_result.errors)}."
    else:
        prompt += "There were no errors."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes embedding job results."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
