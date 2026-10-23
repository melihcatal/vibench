import os
from typing import Dict, Any
from anthropic import Anthropic
from database_models import Document

def record_summary(document: Document) -> str:
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = Anthropic(api_key=anthropic_api_key)

    document_content_str = str(document.content)

    response = client.messages.create(
        model="claude-3-opus-20240229", # Concrete model identifier
        max_tokens=1000,
        messages=[
            {"role": "user", "content": f"Summarize the following document content: {document_content_str}"}
        ]
    )
    return response.content[0].text
