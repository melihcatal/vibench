import os
from model_client import vertex_client
from model_models import LLMRequest, LLMResponse


def answer_question_with_context(
    question: str, context: str, model_name: str = "gemini-pro"
) -> LLMResponse:
    """
    Calls a hosted LLM (Vertex AI's Gemini Pro) to answer a question using provided context.
    """
    prompt = f"""
    Answer the following question based *only* on the provided context.
    If the answer cannot be found in the context, state that you cannot find the answer.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    # Use the shared client
    answer = vertex_client.generate_content(
        model_name=model_name,
        prompt=prompt,
        temperature=0.2,  # Low temperature for factual answers
        max_output_tokens=256,
    )

    return LLMResponse(
        text=answer,
        metadata={"model_provider": "google_vertex_ai", "model_name": model_name},
    )
