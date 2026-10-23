import dashscope

# DashScope Qwen API
# Set your API key in the environment variable DASHSCOPE_API_KEY


def stream_completion(prompt: str):
    """Stream partial output tokens from DashScope Qwen model."""
    client = dashscope.ChatCompletion()
    response = client.chat(
        model="qwen",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in response:
        # Each chunk contains a part of the generated tokens
        yield chunk.choices[0].message.content


if __name__ == "__main__":
    prompt = "Stream this text..."
    for part in stream_completion(prompt):
        print(part, end="", flush=True)
