from model_client import LLMClient
from model_models import LLMRequest, LLMResponse
from typing import Iterator

def stream_completion(prompt: str) -> Iterator[LLMResponse]:
    """Streams partial output tokens from a hosted LLM."""
    llm_client = LLMClient().get_client()
    model = llm_client.GenerativeModel('gemini-pro')

    response_stream = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 1024,
        },
        stream=True
    )

    for chunk in response_stream:
        yield LLMResponse(text=chunk.text, raw_response=chunk)
