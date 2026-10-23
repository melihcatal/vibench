from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from embeddings_client import OPENAI_BASE_URL, get_openai_client
from embeddings_models import EmbeddingResult


SUMMARY_MODEL = "gpt-4o-mini"


def embedding_job_summary(results: Iterable[EmbeddingResult], model: str = SUMMARY_MODEL) -> str:
    result_list = list(results)
    vector_count = len(result_list)
    dimensions = len(result_list[0].vector) if result_list else 0
    sample_sources = [item.source_text for item in result_list[:5] if item.source_text]

    client: OpenAI = get_openai_client()
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"You summarize OpenAI embedding batch jobs from {OPENAI_BASE_URL}."
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            f"Summarize this embedding job in 3 concise sentences. "
                            f"Vector count: {vector_count}. Dimensions: {dimensions}. "
                            f"Sample texts: {sample_sources}"
                        ),
                    }
                ],
            },
        ],
    )
    return response.output_text
