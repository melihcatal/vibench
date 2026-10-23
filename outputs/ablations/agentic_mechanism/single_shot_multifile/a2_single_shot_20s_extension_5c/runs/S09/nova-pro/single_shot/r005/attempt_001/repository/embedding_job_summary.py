import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def summarize_job(job_id):
    response = client.engines.retrieve(engine_id=job_id)
    return response