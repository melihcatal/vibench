import os
import asyncio
from typing import AsyncGenerator, Dict, Any
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model


def summarize_meeting_chunks(
    transcript_stream: AsyncGenerator[Dict[str, Any], None],
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Summarizes live meeting transcript chunks using IBM watsonx.ai Granite model.
    """
    watsonx_client = APIClient(
        api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
    )

    model = Model(
        model_id="ibm/granite-13b-chat-v2",
        params={
            "decoding_method": "greedy",
            "max_new_tokens": 200,
            "min_new_tokens": 50,
        },
        client=watsonx_client,
    )

    buffer = []
    async for chunk in transcript_stream:
        if chunk["type"] == "final":
            buffer.append(chunk["text"])
            if len(buffer) >= 3:
                prompt = (
                    "Summarize the following meeting transcript excerpt in 2-3 sentences:\n\n"
                    f"{' '.join(buffer)}"
                )
                summary = model.generate_text(prompt=prompt)
                yield {"summary": summary, "original_chunks": buffer.copy()}
                buffer = []

    if buffer:
        prompt = (
            "Summarize the following meeting transcript excerpt in 2-3 sentences:\n\n"
            f"{' '.join(buffer)}"
        )
        summary = model.generate_text(prompt=prompt)
        yield {"summary": summary, "original_chunks": buffer.copy()}
