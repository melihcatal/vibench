import os
import json
from model_client import get_gemini_client
from model_models import ChatRequest, ChatResponse


def extract_json(request: ChatRequest) -> ChatResponse:
    genai = get_gemini_client()
    model = genai.GenerativeModel(request.model)
    prompt = f"Extract JSON from the following text. The JSON should contain relevant information related to the text.\n\nText: {request.prompt}\n\nJSON:"
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": request.temperature,
            "max_output_tokens": request.max_output_tokens,
            "response_mime_type": "application/json",  # Specify JSON output
        },
    )
    return ChatResponse(text=response.text)
