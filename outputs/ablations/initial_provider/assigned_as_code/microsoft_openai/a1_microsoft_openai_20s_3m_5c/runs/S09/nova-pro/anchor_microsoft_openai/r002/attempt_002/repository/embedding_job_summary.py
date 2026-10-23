import os
from openai import OpenAI


def summarize_embedding_job_results(job_results, config=None):
    config = config or {}
    with OpenAI(api_key=config.get('api_key') or os.environ['OPENAI_API_KEY']) as client:
        response = client.completions.create(
            model='text-davinci-003',
            prompt=f'Summarize the following embedding job results: {job_results}',
            max_tokens=100
        )
    return {'summary': response.choices[0].text.strip()}