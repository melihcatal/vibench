import os
from collections.abc import Sequence

from openai import OpenAI

DEFAULT_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_embedding_job_results(job_records: Sequence[dict], model: str = DEFAULT_MODEL) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = "Summarize the embedding job results with key counts, failures, and notable patterns.\n\n"
    prompt += "Records:\n"
    prompt += "\n".join(str(record) for record in job_records)
    response = client.responses.create(
        model=model,
        input=prompt,
    )
    return getattr(response, "output_text", "")
