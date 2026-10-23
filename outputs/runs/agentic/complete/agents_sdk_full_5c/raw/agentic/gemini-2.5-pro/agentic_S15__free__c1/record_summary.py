import os
import openai

def summarize_record(record_text: str) -> str:
    """
    Summarizes the text content of a record using the OpenAI API.

    Args:
        record_text: The text to be summarized.

    Returns:
        A string containing the summary.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    
    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Please summarize the following text:\n\n{record_text}"}
            ],
            temperature=0.5,
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return "Error: Summary generation failed."
