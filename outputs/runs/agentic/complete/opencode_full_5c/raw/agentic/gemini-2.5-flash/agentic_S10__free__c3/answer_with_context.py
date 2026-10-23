import os
from model_client import VertexAIModelClient
from model_models import ContextualInferenceRequest, InferenceResponse


def answer_with_context(request: ContextualInferenceRequest) -> InferenceResponse:
    """Calls a hosted LLM to answer a question using provided context."""
    client = VertexAIModelClient(
        model_name="gemini-pro"
    )  # Using google.cloud.aiplatform via VertexAIModelClient

    prompt = (
        f"Answer the following question based only on the provided context. "
        f"If the answer is not in the context, state that you don't know.\n\n"
        f"Context: {request.context}\n\nQuestion: {request.question}\n\nAnswer:"
    )

    response = client.generate_text(
        prompt,
        max_output_tokens=request.max_output_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        top_k=request.top_k,
    )

    generated_text = ""
    safety_attributes = None

    if response.candidates:
        generated_text = response.candidates[0].content.parts[0].text
        safety_attributes = {
            "safety_ratings": [
                sr.to_dict() for sr in response.candidates[0].safety_ratings
            ]
        }

    return InferenceResponse(
        generated_text=generated_text, safety_attributes=safety_attributes
    )
