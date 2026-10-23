# Summarize long text using a hosted LLM via DashScope API
import dashscope


def summarize_text(text: str, model: str = "gpt-4o-mini") -> str:
    """Summarize long text using a hosted LLM via DashScope API.

    Args:
        text: The input text to summarize.
        model: Model identifier for the DashScope endpoint.

    Returns:
        Summarized text.
    """
    client = dashscope.Client(api_key="DASHSCOPE_API_KEY")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": text}],
        temperature=0.2,
    )
    return response.choices[0].message.content
