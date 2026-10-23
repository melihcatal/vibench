import os
from model_client import get_gemini_client
from model_models import ChatRequest, ChatResponse


def summarize_text(request: ChatRequest) -> ChatResponse:
    genai = get_gemini_client()
    model = genai.GenerativeModel(request.model)
    prompt = f"Please summarize the following text: {request.prompt}"
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_output_tokens,
        },
    )
    return ChatResponse(text=response.text)
