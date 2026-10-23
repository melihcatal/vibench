import dashscope

# Provider: DashScope Qwen API


def summarize_text(text: str) -> str:
    client = dashscope.TextChat(
        api_key="${DASHSCOPE_API_KEY}"  # Placeholder for API key
    )
    response = client.chat(
        model="qwen",
        messages=[{"role": "user", "content": text}],
        temperature=0.7,
    )
    return response.choices[0].message.content
