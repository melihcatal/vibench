import dashscope


def stream_completion(prompt: str, max_tokens: int = 200) -> None:
    """Stream token completions from DashScope Qwen model.

    Yields each partial token as it becomes available.
    """
    client = dashscope.TextGeneration(api_key="${DASHSCOPE_API_KEY}")
    response = client.chat(
        model="qwen-plus",
        messages=[{"role": "user", "content": prompt}],
        streaming=True,
        max_tokens=max_tokens,
    )
    for chunk in response.stream():
        # `chunk` contains the next chunk of generated text (could be partial)
        print(chunk.choices[0].message.content, end="", flush=True)
