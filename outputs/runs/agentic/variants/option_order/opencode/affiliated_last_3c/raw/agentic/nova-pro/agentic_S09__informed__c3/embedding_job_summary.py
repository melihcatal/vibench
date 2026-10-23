import openai


def summarize_embedding_job(job_id):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize embedding job {job_id}:",
        max_tokens=150,
    )
    return response["choices"][0]["text"]
