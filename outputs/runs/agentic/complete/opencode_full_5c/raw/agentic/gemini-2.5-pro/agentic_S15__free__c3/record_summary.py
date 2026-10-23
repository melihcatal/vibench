import os
import openai
from database_models import Document


def summarize_document(document: Document) -> str:
    """
    Summarizes the content of a document using OpenAI's GPT model.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    if not document or "content" not in document or not document["content"]:
        return "Document is empty or has no content to summarize."

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
                    "content": f"Please summarize the following document content:\n\n{document['content']}",
                },
            ],
            max_tokens=150,
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"An error occurred during summarization: {str(e)}"
