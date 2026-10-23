import os
from openai import OpenAI

MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")


def embedding_job_summary(job_result):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = f"Summarize this embedding job result clearly and briefly:
{job_result}"
    response = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content
