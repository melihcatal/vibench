from model_client import get_gemini_client
from model_models import LLMRequest, LLMResponse


def summarize_text(request: LLMRequest) -> LLMResponse:
    model = get_gemini_client()
    prompt = f"Please summarize the following text:\n\n{request.prompt}"
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_tokens,
        },
    )
    return LLMResponse(text=response.text, model=request.model)
