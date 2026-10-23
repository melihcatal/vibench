import os
import cohere
from typing import Dict, Any

def summarize_record_text(document_content: str) -> str:
    """
    Summarizes the text content of a document record using the Cohere API.

    :param document_content: The text content to summarize.
    :return: The summarized text, or an error message.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        return "Error: COHERE_API_KEY environment variable not set."

    try:
        co = cohere.Client(api_key)
        response = co.summarize(
            text=document_content,
            model='summarize-xlarge',
            length='medium',
            extractiveness='medium'
        )
        return response.summary
    except cohere.CohereError as e:
        return f"Error from Cohere API: {e}"

