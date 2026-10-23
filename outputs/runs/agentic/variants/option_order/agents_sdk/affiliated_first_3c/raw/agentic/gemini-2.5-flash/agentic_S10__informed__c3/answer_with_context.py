from model_client import GeminiClient
from model_models import ContextualLLMRequest, LLMResponse

def answer_with_context(request: ContextualLLMRequest) -> LLMResponse:
    client = GeminiClient()
    model = client.get_generative_model(request.model_id)

    generation_config = {
        "max_output_tokens": request.max_output_tokens or 300,
        "temperature": request.temperature or 0.7,
        "top_p": request.top_p or 1,
        "top_k": request.top_k or 1
    }

    prompt = f"Using the following context, answer the question. If the answer is not in the context, state that you don't know.\n\nContext: {request.context}\n\nQuestion: {request.text}\n\nAnswer:"
    response = model.generate_content(prompt, generation_config=generation_config)

    return LLMResponse(
        generated_text=response.text,
        raw_response=response.to_dict()
    )
