import os
from anthropic import Anthropic


def answer_with_context(question: str, context: str) -> str:
    """
    Answer a question using provided context with Anthropic Claude.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=api_key)

    prompt = f"""Based on the following context, answer the question. If the answer cannot be found in the context, say "I cannot answer based on the provided context."

Context:
{context}

Question: {question}

Answer:"""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text
