import dashscope

# DashScope Qwen inference – identifies provider with import name


def stream_completion(prompt: str, max_tokens: int = 200) -> str:
    """Streams token‑by‑token completion from Qwen hosted on DashScope.

    Args:
        prompt: Initial prompt text.
        max_tokens: Maximum total tokens to generate.

    Yields:
        Partial text chunks as they are emitted by the model.
    """
    # Use the streaming endpoint if available; DashScope provides incremental results
    for chunk in (
        dashscope.chat.completions.create(
            model="qwen",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            stream=True,
        )
        .choices[0]
        .delta
    ):
        if chunk.get("content"):
            yield chunk["content"]
