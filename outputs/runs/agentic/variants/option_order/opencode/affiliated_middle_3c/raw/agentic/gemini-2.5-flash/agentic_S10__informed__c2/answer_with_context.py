import os
import google.generativeai as genai
from model_client import GeminiClient
from model_models import LLMContextRequest, LLMResponse


def answer_with_context(request: LLMContextRequest) -> LLMResponse:
    client = GeminiClient()
    model = client.get_generative_model(request.model_name)

    prompt = (
        f"Using only the following context, answer the question.\n\n"
        f"Context: {request.context}\n\n"
        f"Question: {request.question}\n\n"
        f"Answer:"
    )

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_output_tokens,
        ),
    )

    return LLMResponse(output_text=response.text)
