import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-5.4-mini")


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _format_job_results(job_results: List[Dict[str, Any]]) -> str:
    lines = []
    for i, item in enumerate(job_results, 1):
        lines.append(f"{i}. {item}")
    return "\n".join(lines)


def summarize_embedding_job_results(
    job_results: List[Dict[str, Any]],
    job_name: Optional[str] = None,
    extra_context: Optional[str] = None,
) -> str:
    prompt_parts = [
        "Summarize the embedding job results concisely.",
    ]
    if job_name:
        prompt_parts.append(f"Job name: {job_name}")
    if extra_context:
        prompt_parts.append(f"Context: {extra_context}")
    prompt_parts.append("Results:")
    prompt_parts.append(_format_job_results(job_results))
    prompt = "\n".join(prompt_parts)
    response = _client().responses.create(
        model=MODEL,
        input=prompt,
    )
    return response.output_text


def summarize_embedding_job_result(
    job_result: Dict[str, Any],
    job_name: Optional[str] = None,
    extra_context: Optional[str] = None,
) -> str:
    return summarize_embedding_job_results([job_result], job_name=job_name, extra_context=extra_context)
