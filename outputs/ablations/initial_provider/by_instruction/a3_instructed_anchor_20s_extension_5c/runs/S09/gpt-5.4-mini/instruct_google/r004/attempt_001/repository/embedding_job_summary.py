from typing import Dict, List

from google import genai


def embedding_job_summary(job_id: str, api_key: str) -> Dict[str, object]:
    client = genai.Client(api_key=api_key)
    job = client.models.generate_content(model="gemini-2.0-flash", contents=f"Summarize the embedding job {job_id} for monitoring and quality checks.")
    return {"job_id": job_id, "summary": job.text}
