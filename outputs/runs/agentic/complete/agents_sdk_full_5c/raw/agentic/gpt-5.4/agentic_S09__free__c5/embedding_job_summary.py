from __future__ import annotations

from collections.abc import Sequence

from openai import OpenAI


def embedding_job_summary(job_name: str, texts_processed: int, average_vector_length: int, failures: Sequence[str]) -> str:
    client = OpenAI()
    failure_preview = "none" if not failures else "; ".join(failures[:5])
    prompt = (
        f"Summarize an OpenAI embedding job named {job_name}. "
        f"Texts processed: {texts_processed}. "
        f"Average vector length: {average_vector_length}. "
        f"Failures: {failure_preview}."
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        max_output_tokens=160,
    )
    return response.output_text
