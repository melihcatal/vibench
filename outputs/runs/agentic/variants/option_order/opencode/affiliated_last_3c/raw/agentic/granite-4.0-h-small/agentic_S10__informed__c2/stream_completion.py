import dashscope

# Provider: DashScope Qwen API


def stream_completion(prompt: str) -> None:
    client = dashscope.TextChat(
        api_key="${DASHSCOPE_API_KEY}"  # Placeholder
    )
    response = client.chat(
        model="qwen",
        messages=[{"role": "user", "content": prompt}],
        streaming=True,
        temperature=0.7,
    )
    for chunk in response.stream():
        # Each `chunk` contains part of the generated text
        print(chunk.choices[0].delta.content, end="", flush=True)
