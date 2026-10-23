from embeddings_client import DEFAULT_CHAT_MODEL, get_client


def embedding_job_summary(job_results: list[dict]) -> str:
    client = get_client()
    prompt = f"Summarize this embedding job results payload succinctly: {job_results}"
    response = client.responses.create(model=DEFAULT_CHAT_MODEL, input=prompt)
    return response.output_text
