import os
from typing import Optional
from model_client import get_dashscope_client
from model_models import ContextualAnswerRequest, ContextualAnswerResponse

def answer_with_context(
    question: str,
    context: str,
    model: str = "qwen-turbo",
    temperature: float = 0.7,
) -> str:
    """
    Answer a question using provided context with DashScope Qwen model.
    
    Args:
        question: Question to answer.
        context: Contextual information to use for answering.
        model: Model identifier (e.g., "qwen-turbo", "qwen-plus").
        temperature: Sampling temperature.
    
    Returns:
        Generated answer as a string.
    """
    client = get_dashscope_client()
    
    prompt = (
        f"Answer the question based on the context below. "
        f"If the answer is not in the context, say 'I don't know'.\n\n"
        f"Context: {context}\n\n"
        f"Question: {question}"
    )
    
    request = ContextualAnswerRequest(
        model=model,
        prompt=prompt,
        temperature=temperature,
    )
    
    response = client.call_model(request)
    return ContextualAnswerResponse(**response).output