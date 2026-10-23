import os
import requests


def summarize_embedding_job(job_id, config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["SUMMARIZATION_API_KEY"]
    response = requests.get(f"https://api.summarization.com/v1/jobs/{job_id}", headers={"Authorization": f"Bearer {api_key}"})
    response.raise_for_status()
    return response.json()