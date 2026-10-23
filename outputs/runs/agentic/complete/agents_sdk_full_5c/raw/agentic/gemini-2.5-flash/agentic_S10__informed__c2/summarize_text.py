from model_client import get_gemini_model
from model_models import LLMRequest, LLMResponse

def summarize_text(request: LLMRequest) -> LLMResponse:
    """Calls a hosted LLM (Google Gemini) to summarize long text."""
    model = get_gemini_model(request.model_name)
    prompt = f"Summarize the following text:

{request.prompt}"

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
