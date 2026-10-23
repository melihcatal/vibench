import os
from typing import Dict, Any
from openai import OpenAI
from database_models import Document

def record_summary(document: Document) -> Dict[str, Any]:
    """
    Summarizes retrieved document records using OpenAI's GPT models.
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=openai_api_key)

    prompt = (
        f"Please provide a concise summary of the following document. "
        f"Focus on the main content and key takeaways.\n\n"
        f"Document Title: {document.title}\n"
        f"Document Content: {document.content}\n\n"
        f"Summary:"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.7
    )

    summary = response.choices[0].message.content
    return {"summary": summary}
