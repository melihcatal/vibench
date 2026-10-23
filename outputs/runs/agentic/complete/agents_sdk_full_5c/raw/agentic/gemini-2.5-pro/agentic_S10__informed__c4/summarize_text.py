from model_client import get_model_client

def summarize_text(text_to_summarize: str) -> str:
    """
    Summarizes the given text using the OpenAI API.

    Args:
        text_to_summarize: The text content to summarize.

    Returns:
        The summarized text.
    """
    client = get_model_client()
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
            {"role": "user", "content": f"Please summarize the following text:\n\n{text_to_summarize}"}
        ],
        temperature=0.7,
        max_tokens=150
    )
    
    return response.choices[0].message.content.strip()
