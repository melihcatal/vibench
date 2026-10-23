from model_client import get_gemini_model
from model_models import LLMRequest, LLMResponse

def answer_with_context(request: LLMRequest) -> LLMResponse:
    """Calls a hosted LLM (Google Gemini) to answer a question using provided context."""
    if not request.context:
        raise ValueError("Context must be provided for answer_with_context.")

    model = get_gemini_model(request.model_name)
    prompt = (
        f"Using the following context, answer the question. "
        f"If the answer is not in the context, state that you don't know.\n\n"
        f"Context: {request.context}\n\n"
        f"Question: {request.prompt}\n"
        f"Answer:"
    )

    generation_config = {
        "max_output_tokens": request.max_output_tokens,
        "temperature": request.temperature,
        "top_p": request.top_p,
        "top_k": request.top_k,
    }
    if request.stop_sequences:
        generation_config["stop_sequences"] = request.stop_sequences

    response = model.generate_content(
        prompt,
        generation_config=generation_config,
    )

    # Google Gemini API identifies with 'google.generativeai'
    # Model family is 'gemini-pro'
    # Provider API hostname is implicitly handled by the SDK
    return LLMResponse(
        text=response.text,
        finish_reason=response.candidates[0].finish_reason.name if response.candidates else None,
        token_count={
            "prompt_tokens": model.count_tokens(prompt).total_tokens,
            "completion_tokens": model.count_tokens(response.text).total_tokens,
        }
    )
