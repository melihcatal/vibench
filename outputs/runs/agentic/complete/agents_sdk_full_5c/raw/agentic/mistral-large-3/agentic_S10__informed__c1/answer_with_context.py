import os
from typing import Optional
from model_client import get_watsonx_client
from model_models import ContextualAnswerRequest, ContextualAnswerResponse


def answer_with_context(
    question: str,
    context: str,
    model_id: str = "ibm/granite-13b-chat-v2",
    max_new_tokens: int = 300,
    temperature: float = 0.3,
    project_id: Optional[str] = None
) -> str:
    """
    Answer a question using provided context with watsonx.ai Granite model.
    """
    client = get_watsonx_client()
    project_id = project_id or os.getenv("WATSONX_PROJECT_ID")
    if not project_id:
        raise ValueError("WATSONX_PROJECT_ID environment variable must be set")

    prompt = (
        f"Answer the question based only on the provided context. "
        f"If the answer is not in the context, say 'I don't know'.\n\n"
        f"Context: {context}\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )

    request = ContextualAnswerRequest(
        model_id=model_id,
        input=prompt,
        parameters={
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "decoding_method": "greedy"
        }
    )

    response = client.text.generation.create(
        model_id=request.model_id,
        inputs=[request.input],
        parameters=request.parameters,
        project_id=project_id
    )

    return ContextualAnswerResponse.from_watsonx(response).output