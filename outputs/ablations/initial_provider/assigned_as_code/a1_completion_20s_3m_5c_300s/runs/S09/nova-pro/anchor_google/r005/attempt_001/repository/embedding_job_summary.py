import os

from google import genai


def embedding_job_summary(job_id, config=None):
    config = config or {}
    with genai.Client(api_key=config.get('api_key') or os.environ['GOOGLE_API_KEY']) as client:
        job_details = client.jobs.get(job_id=job_id)
    return job_details