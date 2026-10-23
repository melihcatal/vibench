from model_client import GeminiClient
from model_models import ChatRequest, ChatResponse


def answer_with_context(
    question: str, context: str, request: ChatRequest
) -> ChatResponse:
    client = GeminiClient()
    model = client.get_model(request.model)
    prompt = f"Using the following context, answer the question.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_output_tokens,
        },
    )
    return ChatResponse(text=response.text)
