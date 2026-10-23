import json
from model_client import create_client


def summarize_text(text: str, model: str = "gpt-4o-mini") -> str:
    """Summarize long text using a hosted LLM.

    Args:
        text (str): The long text to summarize.
        model (str): The model family to use (default: gpt-4o-mini).

    Returns:
        str: The generated summary.
    """
    client = create_client(model)
    prompt = f"Summarize the following text in no more than 3 sentences:\n\n{text}"
    response = client.chat_completion(messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content.strip()
