from model_client import get_gemini_client
from model_models import LLMContextRequest, LLMResponse


def answer_with_context(request: LLMContextRequest) -> LLMResponse:
    model = get_gemini_client()
    prompt = (
        f"Given the following context, answer the question. "
        f"If the answer is not in the context, state that you don't know.\n\n"
        f"Context: {request.context}\n\n"
        f"Question: {request.question}\n\n"
        f"Answer:"
    )
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_tokens,
        },
    )
    return LLMResponse(text=response.text, model=request.model)
