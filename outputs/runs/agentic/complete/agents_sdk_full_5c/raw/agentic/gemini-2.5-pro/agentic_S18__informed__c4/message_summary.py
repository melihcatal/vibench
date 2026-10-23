import os
from openai import OpenAI

def summarize_message_text(text_content: str) -> str:
    """
    Summarizes the provided text using the OpenAI Chat Completions API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Please summarize the following text:\n\n{text_content}"}
            ],
            temperature=0.5,
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return "Error: Summary generation failed."
