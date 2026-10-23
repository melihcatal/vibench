from model_client import get_openai_client


def summarize_text(long_text: str) -> str:
    """
    Calls a hosted LLM to summarize long text.
    """
    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text.",
            },
            {
                "role": "user",
                "content": f"Please summarize the following text:\n\n{long_text}",
            },
        ],
        temperature=0.7,
        max_tokens=150,
    )

    if response.choices:
        return response.choices[0].message.content.strip()
    return ""
