import os
from openai import OpenAI


def summarize_embedding_job(job_results):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Summarize this embedding job result set concisely: {job_results}"
    response = client.chat.completions.create(model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"), messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content
