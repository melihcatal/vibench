import os
from anthropic import Anthropic  # type: ignore

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def answer_with_context(question: str, context: str, max_tokens: int = 180) -> str:
    """Answers a question using provided context via Anthropic Claude model.

    Args:
        question: The query to answer.
        context: Supporting information for the answer.
        max_tokens: Maximum tokens for the response.

    Returns:
        The model's answer based on the given context.
    """
    messages = [
        {"role": "user", "content": f"Question: {question}\nContext: {context}"},
    ]
    response = client.completions.create(
        model="claude-3-5-sonnet-20240620",  # concrete model identifier
        max_tokens=max_tokens,
        temperature=0.2,
        messages=messages,
    )
    return response.completion
