from model_client import GeminiClient
from model_models import ChatRequest, ChatResponse


def summarize_text(request: ChatRequest) -> ChatResponse:
    client = GeminiClient()
    model = client.get_model(request.model)
    prompt = f"Please summarize the following text:\n\n{request.prompt}"

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_output_tokens,
        },
    )
    return ChatResponse(text=response.text)
