import os
import requests

def embedding_job_summary(job_id):
    api_key = os.getenv('DIRECT_EMBEDDINGS_API_KEY')
    api_url = f'https://api.directembeddings.com/v1/jobs/{job_id}'
    response = requests.get(api_url, headers={'Authorization': f'Bearer {api_key}'})
    response.raise_for_status()
    return response.json()