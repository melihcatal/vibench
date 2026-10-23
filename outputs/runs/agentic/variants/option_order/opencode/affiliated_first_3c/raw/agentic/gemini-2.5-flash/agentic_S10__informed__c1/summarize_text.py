import os
from model_client import GeminiClient
from model_models import ChatRequest, ChatResponse


def summarize_text(text: str) -> ChatResponse:
    client = GeminiClient()
    model = client.get_generative_model("gemini-pro")
    safety_settings = client.get_safety_settings()

    prompt = f"Please summarize the following text:\n\n{text}"
    generation_config = {"temperature": 0.7, "max_output_tokens": 256}
    response = model.generate_content(
        prompt, safety_settings=safety_settings, generation_config=generation_config
    )
    return ChatResponse(text=response.text)
