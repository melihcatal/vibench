import dashscope


def embedding_job_summary(job_results):
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    response = dashscope.TextGeneration.create(
        model="text-generation-v1",
        prompt=f"Summarize the following embedding job results: {job_results}",
    )
    return response.output.text
