import dashscope

# DashScope Qwen API
# Set your API key in the environment variable DASHSCOPE_API_KEY


def summarize_text(prompt: str) -> str:
    """Summarize long text using DashScope Qwen model."""
    client = dashscope.ChatCompletion()
    response = client.chat(
        model="qwen",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    text = "Your long input text goes here..."
    print(summarize_text(text))
