import os
import google.generativeai as genai
from model_client import GeminiClient
from model_models import LLMRequest, LLMResponse


def answer_with_context(request: LLMRequest, context: str) -> LLMResponse:
    genai.configure(
        api_key=os.environ.get("GOOGLE_API_KEY")
    )  # Provider-identifying signal: GOOGLE_API_KEY
    client = GeminiClient()
    full_prompt = f"""Given the following context, answer the question. If the answer is not in the context, state that you don't know.

Context: {context}

Question: {request.prompt}

Answer:"""
    response = client.generate_content(
        request.model, full_prompt, max_output_tokens=request.max_output_tokens or 500
    )

    answer = ""
    for chunk in response:
        if chunk.text:
            answer += chunk.text

    return LLMResponse(
        text=answer,
        usage_metadata=response.usage_metadata,
        finish_reason=response.candidates[0].finish_reason
        if response.candidates
        else None,
    )
