import os
from openai import OpenAI

# The OpenAI client looks for the OPENAI_API_KEY environment variable by default.
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def summarize_record(record_content: str) -> str:
    """
    Summarizes the content of a document record using the OpenAI Chat Completions API.

    Args:
        record_content: The text content of the record to summarize.

    Returns:
        A string containing the summary.
    """
    if not record_content:
        return ""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Specify the concrete model
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text concisely.",
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following text in one or two sentences:\n\n{record_content}",
                },
            ],
            temperature=0.5,
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        print(f"An error occurred while communicating with the OpenAI API: {e}")
        return "Error: Summary generation failed."
