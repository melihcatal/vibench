import os
from dashscope import TextGeneration


def embedding_job_summary(job_results: list) -> str:
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")
    response = TextGeneration.call(
        model="text-generation-v1",
        prompt=f"Summarize the following job results: {job_results}",
        api_key=api_key,
    )
    return response["output"]["text"]
