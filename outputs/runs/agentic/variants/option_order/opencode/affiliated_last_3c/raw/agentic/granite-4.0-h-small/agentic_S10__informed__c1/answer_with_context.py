# Answer a question using provided context via Anthropic Messages API
import anthropic


def answer_with_context(
    question: str, context: str, model: str = "claude-3-opus-20240229"
) -> str:
    """Answer a question with additional context using Anthropic's Claude model.

    Args:
        question: The user's query.
        context: Background information for the answer.
        model: Claude model identifier.

    Returns:
        The answer string.
    """
    client = anthropic.Anthropic(api_key="ANTHROPIC_API_KEY")
    response = client.messages.create(
        model=model,
        max_tokens=512,
        temperature=0.0,
        messages=[
            {"role": "user", "content": question},
            {"role": "assistant", "content": context},
        ],
    )
    return response.content[0].text
