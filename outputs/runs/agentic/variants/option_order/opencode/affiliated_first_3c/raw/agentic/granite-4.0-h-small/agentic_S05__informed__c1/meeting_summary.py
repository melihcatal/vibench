"""
Summarizes live meeting transcript chunks using watsonx.ai Granite model.
Uses SDK: ibm-watsonx-ai (or REST fallback).
Credentials: WATSONX_API_KEY, WATSONX_PROJECT_ID
"""

import os
import asyncio
import json
from ibm_watsonx_ai import Client
from ibm_watsonx_ai.genai import ChatConfig, FoundationModelChatOptions

MODEL_ID = "granite-4-0-h-small"  # exact model identifier


async def summarize_chunks(chunks: list[str]) -> str:
    """Summarizes a list of transcript chunks into a meeting summary."""
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    client = Client(
        base_url="https://api.watsonx.ai", api_key=api_key, project_id=project_id
    )
    prompt = "\\n".join(chunks)
    chat_config = ChatConfig(model_id=MODEL_ID, temperature=0.2)
    options = FoundationModelChatOptions(
        chat_config=chat_config,
        system_prompt="You are a meeting summarizer. Produce a 3-5 sentence summary, highlighting key decisions.",
    )
    response = client.generation.generate_content(
        prompt=prompt, foundation_model_options=options
    )
    summary = response.generations[0].text
    return summary


async def live_summary(source_async_gen: Iterator[str]) -> None:
    """Collects chunks and prints a live summary after 3 chunks."""
    accumulated = []
    async for chunk in source_async_gen:
        accumulated.append(chunk)
        if len(accumulated) >= 3:
            summary = await summarize_chunks(accumulated)
            print("--- Summary so far ---")
            print(summary)
            accumulated = []


def get_source() -> Iterator[str]:
    """Dummy async generator simulating live caption source."""
    for i in range(1, 7):
        await asyncio.sleep(0.5)
        yield f"Chunk {i}: Team agreed to deliver by Q4. Discussion on budget."


if __name__ == "__main__":
    asyncio.run(live_summary(get_source()))
