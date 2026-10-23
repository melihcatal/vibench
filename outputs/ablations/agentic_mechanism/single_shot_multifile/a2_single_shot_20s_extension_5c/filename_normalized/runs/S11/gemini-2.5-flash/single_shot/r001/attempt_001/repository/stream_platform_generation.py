from typing import Generator
from model_models import CompletionRequest, CompletionResponse
from model_client import get_anthropic_client
import anthropic

def stream_anthropic_generation(request: CompletionRequest) -> Generator[CompletionResponse, None, None]:
    client = get_anthropic_client()
    model_to_use = request.model_name if request.model_name != "default" else "claude-3-opus-20240229"
    try:
        with client.messages.stream(
            model=model_to_use,
            max_tokens=1024,
            messages=[{"role": "user", "content": request.prompt}],
        ) as stream:
            for text_chunk in stream.text_stream:
                yield CompletionResponse(text=text_chunk, provider_response=stream.current_message.model_dump())
    except anthropic.APIError as e: raise RuntimeError(f"Anthropic API error: {e}")