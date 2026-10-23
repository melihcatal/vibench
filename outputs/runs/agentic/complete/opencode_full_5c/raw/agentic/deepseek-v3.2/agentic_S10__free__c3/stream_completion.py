from typing import Generator, Optional
from openai import OpenAI
from model_client import get_llm_client
from model_models import StreamCompletionRequest, StreamChunk


def stream_completion(
    prompt: str, model: Optional[str] = None
) -> Generator[StreamChunk, None, None]:
    """
    Stream partial output tokens from a hosted LLM.

    Args:
        prompt: The prompt to complete
        model: Optional specific model to use

    Returns:
        Generator yielding StreamChunk objects with partial text
    """
    client = get_llm_client()

    model_to_use = model or "gpt-4o-mini"

    try:
        stream = client.chat.completions.create(
            model=model_to_use,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.7,
            stream=True,
        )

        full_text = ""

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                text_chunk = chunk.choices[0].delta.content
                full_text += text_chunk

                yield StreamChunk(
                    chunk_text=text_chunk,
                    full_text_so_far=full_text,
                    model_used=model_to_use,
                    provider="openai",
                )

    except Exception as e:
        raise Exception(f"Failed to stream completion: {str(e)}")
