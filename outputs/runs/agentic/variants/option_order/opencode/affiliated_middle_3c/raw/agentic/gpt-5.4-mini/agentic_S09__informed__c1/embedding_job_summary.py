from openai import OpenAI


def summarize_embedding_job(job_results: list[dict], model: str = 'gpt-4.1-mini') -> str:
    client = OpenAI()
    prompt = 'Summarize this embedding job: ' + str(job_results)
    response = client.responses.create(model=model, input=prompt)
    return response.output_text
