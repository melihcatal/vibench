import os
import openai

def summarize_record(text_content: str) -> str:
    """
    Summarizes the provided text content using the OpenAI Chat Completions API.

    Args:
        text_content: The text from the document record to be summarized.

    Returns:
        A string containing the summary.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text concisely."
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following text:\n\n{text_content}"
                }
            ],
            temperature=0.5,
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except openai.APIError as e:
        # Handle API errors (e.g., rate limits, server errors)
        return f"An OpenAI API error occurred: {e}"
