import dashscope

DASHSCOPE_API_KEY = "$DASHSCOPE_API_KEY"


def summarize_text(text):
    client = dashscope.ChatCompletion(api_key=DASHSCOPE_API_KEY, model="qwen-72b-chat")
    response = client.chat(
        messages=[{"role": "user", "content": text}], max_tokens=150, temperature=0.7
    )
    return response.choices[0].message.content
