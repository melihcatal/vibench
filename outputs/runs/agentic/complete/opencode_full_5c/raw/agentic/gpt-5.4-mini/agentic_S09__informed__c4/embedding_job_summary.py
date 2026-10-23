from openai import OpenAI


def summarize_embedding_job(job_text: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1-mini", input=f"Summarize this embedding job result: {job_text}"
    )
    return response.output_text
