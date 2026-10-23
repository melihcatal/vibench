import dashscope


def summarize_text(text: str, max_tokens: int = 150) -> str:
    """Summarize the input text using the DashScope Qwen model.

    Args:
        text (str): The text to summarize.
        max_tokens (int, optional): Maximum token count for the summary.

    Returns:
        str: The generated summary.
    """
    client = dashscope.TextGeneration(
        api_key="${DASHSCOPE_API_KEY}",  # Placeholder for environment variable
    )
    response = client.chat(
        model="qwen-plus",
        messages=[{"role": "user", "content": text}],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content
