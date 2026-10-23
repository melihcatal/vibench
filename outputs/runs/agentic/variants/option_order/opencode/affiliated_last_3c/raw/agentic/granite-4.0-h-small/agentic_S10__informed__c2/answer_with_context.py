import dashscope

# Provider: DashScope Qwen API


def answer_with_context(context: str, question: str) -> str:
    client = dashscope.TextChat(
        api_key="${DASHSCOPE_API_KEY}"  # Placeholder
    )
    response = client.chat(
        model="qwen",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": question},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content
