import os
from model_client import vertex_client
from model_models import LLMRequest, LLMResponse


def summarize_text(text: str, model_name: str = "gemini-pro") -> LLMResponse:
    """
    Calls a hosted LLM (Vertex AI's Gemini Pro) to summarize long text.
    """
    prompt = f"Summarize the following text:\n\n{text}"

    # Use the shared client
    summary = vertex_client.generate_content(
        model_name=model_name,
        prompt=prompt,
        temperature=0.3,  # Lower temperature for more factual summary
        max_output_tokens=512,
    )

    return LLMResponse(
        text=summary,
        metadata={"model_provider": "google_vertex_ai", "model_name": model_name},
    )
