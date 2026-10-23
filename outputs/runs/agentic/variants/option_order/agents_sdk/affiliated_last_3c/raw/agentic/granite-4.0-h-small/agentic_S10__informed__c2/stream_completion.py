import os
import json
from model_client import get_llm_client
from model_models import LLMRequest, LLMResponse

def stream_completion(prompt: str, model_family: str = "gpt-4"):
    """Stream partial output tokens from a hosted LLM.

    Yields:
        str: Incremental text chunks as the model generates them.
    """
    client = get_llm_client(model_family)
    request = LLMRequest(
        prompt=prompt,
        model=model_family,
        temperature=0.7,
        max_tokens=1024,
        stream=True,
    )
    # Assuming the client provides an async/iterable generator for streaming
    async for chunk in client.chat_completion_stream(request):
        # Chunk may be an object with .content field
        yield chunk.choices[0].message.content.strip() if chunk.choices else ""

if __name__ == "__main__":
    demo = "Write the first three paragraphs of a short story about a mysterious lighthouse."
    print("Streaming completion from", demo[:30], "...")
    for part in stream_completion(demo, model_family="gpt-4"):
        print(part, end="")