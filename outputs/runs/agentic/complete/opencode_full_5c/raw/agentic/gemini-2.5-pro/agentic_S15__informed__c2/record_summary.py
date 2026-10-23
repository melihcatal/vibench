import os
import openai
from database_models import Document


def record_summary(record: Document) -> str:
    """
    Summarizes the content of a document record using OpenAI.

    Args:
        record: The document record to summarize.

    Returns:
        A string containing the summary.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    content_to_summarize = record.get("content", "")
    if not content_to_summarize:
        return "Record has no content to summarize."

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes documents.",
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following document content:\n\n{content_to_summarize}",
                },
            ],
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary.strip()
    except Exception as e:
        return f"Error generating summary: {e}"
