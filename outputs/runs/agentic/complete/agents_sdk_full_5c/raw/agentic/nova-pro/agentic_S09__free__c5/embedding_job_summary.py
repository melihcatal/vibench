import os
from cohere import Client

co = Client(os.getenv('COHERE_API_KEY'))

def summarize_job(job_id):
    job = co.get_job(job_id)
    return job.status, job.result
