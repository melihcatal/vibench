import os
import cohere
from typing import Dict, Any


def summarize_record(record: Dict[str, Any]) -> str:
    """
    Summarizes the content of a document record using Cohere.
    """
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(cohere_api_key)

    content = record.get("content", "")
    if not content:
        return "No content to summarize."

    response = co.summarize(
        text=content, model="command", length="medium", extractiveness="medium"
    )

    return response.summary
