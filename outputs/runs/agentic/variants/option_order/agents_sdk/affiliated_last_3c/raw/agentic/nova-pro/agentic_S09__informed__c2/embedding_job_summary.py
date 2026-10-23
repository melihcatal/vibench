import os
from dashscope import Generation

def summarize_embedding_job(job_id):
    response = Generation.call(model='qwen-turbo', prompt=f'Summarize the embedding job with ID {job_id}.', api_key=os.getenv('DASHSCOPE_API_KEY'))
    return response.output.text