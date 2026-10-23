import os
import openai
from database_models import Document


def record_summary(document: Document) -> str:
    """
    Summarizes the content of a document using OpenAI's GPT-3.5 Turbo.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not document.content:
        return ""

    prompt = f"Summarize the following document content:\n\n{document.content}"

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes documents.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
    )
    summary = response.choices[0].message.content
    return summary.strip() if summary else ""
