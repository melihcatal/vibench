import os
from openai import OpenAI
from database_models import Document


def record_summary(record: Document) -> str:
    """
    Summarizes a document record using OpenAI's GPT model.

    :param record: The document record to summarize.
    :return: A string containing the summary.
    """
    if not record or "content" not in record:
        return ""

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"Summarize the following document content in one sentence:\n\n{record['content']}"

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o-mini",
    )

    return chat_completion.choices[0].message.content or ""
