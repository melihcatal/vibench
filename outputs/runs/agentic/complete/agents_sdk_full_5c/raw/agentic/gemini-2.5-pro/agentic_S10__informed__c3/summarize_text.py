from model_client import get_client

def summarize(text: str) -> str:
    """
    Summarizes the given text using an OpenAI model.
    """
    client = get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
        ],
        temperature=0.7,
        max_tokens=150,
    )
    summary = response.choices[0].message.content
    return summary.strip() if summary else ""
