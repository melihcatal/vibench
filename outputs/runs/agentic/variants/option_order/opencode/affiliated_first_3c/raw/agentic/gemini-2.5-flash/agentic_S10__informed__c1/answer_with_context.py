import os
from model_client import GeminiClient
from model_models import ChatRequest, ChatResponse


def answer_with_context(question: str, context: str) -> ChatResponse:
    client = GeminiClient()
    model = client.get_generative_model("gemini-pro")
    safety_settings = client.get_safety_settings()

    prompt = f"Using the following context, answer the question. If the answer is not in the context, state that you don't know.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
    generation_config = {"temperature": 0.3, "max_output_tokens": 512}
    response = model.generate_content(
        prompt, safety_settings=safety_settings, generation_config=generation_config
    )
    return ChatResponse(text=response.text)
