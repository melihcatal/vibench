import os
import openai
from typing import Dict

# Requires OPENAI_API_KEY environment variable to be set.
# The client automatically reads the key from the environment.
client = openai.OpenAI()

def summarize_record(record: Dict[str, any]) -> str:
    """
    Summarizes the content of a document record using the OpenAI API.

    Args:
        record: A dictionary representing the document record.
                It should have a 'content' key.

    Returns:
        A string containing the summary of the document's content.
    """
    content_to_summarize = record.get("content", "")
    if not content_to_summarize:
        return "No content to summarize."

    try:
        # Using a specific model identifier like "gpt-3.5-turbo"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
                {"role": "user", "content": f"Please summarize the following document content:\n\n{content_to_summarize}"}
            ],
            temperature=0.5,
        )
        summary = response.choices[0].message.content
        return summary.strip()
    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return "Failed to generate summary."
