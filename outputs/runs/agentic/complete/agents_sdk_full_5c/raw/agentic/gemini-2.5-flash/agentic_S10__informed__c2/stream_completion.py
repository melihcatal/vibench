from model_client import get_gemini_model
from model_models import LLMRequest
from typing import Iterator

def stream_completion(request: LLMRequest) -> Iterator[str]:
    """Streams partial output tokens from a hosted LLM (Google Gemini)."""
    model = get_gemini_model(request.model_name)

    generation_config = {
        "max_output_tokens": request.max_output_tokens,
        "temperature": request.temperature,
        "top_p": request.top_p,
        "top_k": request.top_k,
    }
    if request.stop_sequences:
        generation_config["stop_sequences"] = request.stop_sequences

    # Google Gemini API identifies with 'google.generativeai'
    # Model family is 'gemini-pro'
    # Provider API hostname is implicitly handled by the SDK
    responses = model.generate_content(
        request.prompt,
        generation_config=generation_config,
        stream=True,
    )

    for response in responses:
        yield response.text
