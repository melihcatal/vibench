from model_client import GeminiClient
from model_models import LLMRequest, LLMResponse

def summarize_text(request: LLMRequest) -> LLMResponse:
    client = GeminiClient()
    model = client.get_generative_model(request.model_id)

    generation_config = {
        "max_output_tokens": request.max_output_tokens or 200,
        "temperature": request.temperature or 0.7,
        "top_p": request.top_p or 1,
        "top_k": request.top_k or 1
    }

    prompt = f"Please summarize the following text:\n\n{request.text}"
    response = model.generate_content(prompt, generation_config=generation_config)

    return LLMResponse(
        generated_text=response.text,
        raw_response=response.to_dict()
    )
