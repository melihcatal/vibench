import os
import google.generativeai as genai
from model_client import GeminiClient
from model_models import LLMRequest, LLMResponse


def summarize_text(request: LLMRequest) -> LLMResponse:
    client = GeminiClient()
    model = client.get_generative_model(request.model_name)

    prompt = f"Summarize the following text:\n\n{request.text_content}"

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_output_tokens,
        ),
    )

    return LLMResponse(output_text=response.text)
