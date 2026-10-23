import dashscope

# Provider: DashScope Qwen API


def extract_json(text: str) -> dict:
    client = dashscope.TextChat(
        api_key="${DASHSCOPE_API_KEY}"  # Placeholder
    )
    response = client.chat(
        model="qwen",
        messages=[{"role": "user", "content": text}],
        temperature=0.0,
        max_tokens=200,
    )
    # Expecting the model to reply with a JSON blob
    return response.choices[0].message.content
