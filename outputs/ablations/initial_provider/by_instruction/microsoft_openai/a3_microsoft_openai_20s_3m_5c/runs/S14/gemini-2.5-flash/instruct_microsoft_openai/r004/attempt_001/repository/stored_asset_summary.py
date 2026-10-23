import os
from openai import OpenAI

def summarize_asset_content(text: str) -> str:
    """
    Summarizes content extracted from a stored asset using OpenAI's GPT models.

    Args:
        text (str): The text content to summarize.

    Returns:
        str: The summarized text.
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=openai_api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using a common, cost-effective model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
            ]
        )
        if response.choices:
            return response.choices[0].message.content.strip()
        else:
            return "Summary generation failed."
    except Exception as e:
        return f"An error occurred during summarization: {e}"
