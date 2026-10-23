import os
from model_client import get_gemini_client
from model_models import ChatRequest, ChatResponse


def answer_with_context(request: ChatRequest, context: str) -> ChatResponse:
    genai = get_gemini_client()
    model = genai.GenerativeModel(request.model)
    prompt = f"Using the following context, answer the question: {request.prompt}\n\nContext: {context}"
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_output_tokens,
        },
    )
    return ChatResponse(text=response.text)
