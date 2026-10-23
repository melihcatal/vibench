from openai import OpenAI

from embeddings_client import get_client, get_embedding_model


def embedding_job_summary(job_results):
    client = get_client()
    model = get_embedding_model()
    summary_prompt = (
        f"Summarize this embedding job result set for model {model}: {job_results}"
    )
    response = client.responses.create(model="gpt-5.4-mini", input=summary_prompt)
    return response.output_text
