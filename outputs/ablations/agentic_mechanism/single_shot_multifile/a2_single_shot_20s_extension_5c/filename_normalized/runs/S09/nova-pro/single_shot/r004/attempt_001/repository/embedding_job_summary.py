import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def summarize_embedding_job(job_id):
    response = openai.Engine.retrieve(job_id)
    return response['summary']