import os
import json
from model_client import get_llm_client
from model_models import LLMRequest, LLMResponse

def answer_with_context(question: str, context: str, model_family: str = "gpt-4") -> str:
    """Answer a question using provided context with a hosted LLM.

    Args:
        question (str): The user question.
        context (str): Background information to ground the answer.
        model_family (str): Identifier for the LLM model family.

    Returns:
        str: The answer.
    """
    client = get_llm_client(model_family)
    request = LLMRequest(
        prompt=f"Given the following context, answer the question in a concise sentence.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:",
        model=model_family,
        temperature=0.2,
        max_tokens=256,
    )
    response = client.chat_completion(request)
    return str(response.choices[0].message.content).strip()

if __name__ == "__main__":
    ctx = "The Eiffel Tower was built between 1887 and 1889 as the entrance arch for the 1889 World's Fair."
    q = "When was the Eiffel Tower completed?"
    print(answer_with_context(q, ctx, model_family="gpt-4"))