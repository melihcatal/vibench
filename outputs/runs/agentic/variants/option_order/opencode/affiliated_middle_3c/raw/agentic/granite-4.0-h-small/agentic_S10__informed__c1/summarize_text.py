import dashscope

# DashScope Qwen inference – identifies provider with import name


def summarize_text(text: str, max_tokens: int = 150) -> str:
    """Summarizes long input text using Qwen hosted on DashScope.\n\n    Args:\n        text: The source text to summarize.\n        max_tokens: Maximum token length for the generated summary.\n\n    Returns:\n        A concise summary string.\n"""
    response = dashscope.chat.completions.create(
        model="qwen",  # hosted Qwen model ID on DashScope
        messages=[{"role": "user", "content": text}],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content
