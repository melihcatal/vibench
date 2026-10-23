import os
from ibm_watsonx_ai import WatsonxAI

client = WatsonxAI(
    api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
)


def summarize_embedding_job(job_id: str) -> str:
    response = client.get_embedding_job(job_id=job_id)
    return response["summary"]
