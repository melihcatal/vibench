import os
import openai

def summarize_record_content(content: str) -> str:
    """
    Summarizes the given text content using the OpenAI Chat Completions API.

    :param content: The text content of the document record to summarize.
    :return: A string containing the summary.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                {"role": "user", "content": f"Please summarize the following content:\n\n{content}"}
            ],
            temperature=0.5,
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except openai.APIError as e:
        print(f"OpenAI API error: {e}")
        raise
