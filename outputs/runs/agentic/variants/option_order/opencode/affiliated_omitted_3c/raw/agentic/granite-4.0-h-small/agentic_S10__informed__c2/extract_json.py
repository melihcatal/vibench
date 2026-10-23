import dashscope

# DashScope Qwen API
# Set your API key in the environment variable DASHSCOPE_API_KEY


def extract_json(prompt: str) -> dict:
    """Extract structured JSON from text using DashScope Qwen model."""
    client = dashscope.ChatCompletion()
    response = client.chat(
        model="qwen",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.parse_json()


if __name__ == "__main__":
    text = "Provide instructions here for JSON extraction"
    print(extract_json(text))
