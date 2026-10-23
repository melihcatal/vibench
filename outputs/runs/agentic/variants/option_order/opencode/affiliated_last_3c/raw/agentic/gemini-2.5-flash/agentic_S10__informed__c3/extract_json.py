from model_client import GeminiClient
from model_models import ChatRequest, ChatResponse


def extract_json(request: ChatRequest) -> ChatResponse:
    client = GeminiClient()
    model = client.get_model(request.model)
    prompt = f"Extract JSON object from the following text. The JSON object should represent key information in the text.\n\nText: {request.prompt}\n\nJSON:"

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_output_tokens,
        },
    )
    return ChatResponse(text=response.text)
