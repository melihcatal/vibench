import os
from openai import OpenAI

def summarize_record(text: str, max_length: int = 50) -> str:
    """
    Summarizes the text content of a document record using OpenAI.

    :param text: The text to summarize.
    :param max_length: The desired maximum length of the summary.
    :return: The summarized text.
    """
    if not text:
        return ""

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following text in approximately {max_length} words: {text}"}
            ],
            temperature=0.5,
            max_tokens=max_length + 20, # Allow some buffer
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"An error occurred with OpenAI summarization: {e}")
        return "Summary not available."
