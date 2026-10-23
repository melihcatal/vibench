import os
from typing import List

import anthropic

def summarize_embedding_job(embedding_details: List[str]) -> str:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    context_text = "\n".join(embedding_details)

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Please summarize the following details about an embedding job. "
                    f"Focus on key metrics, number of items processed, any errors, and overall success:\n\n{context_text}"
                )
            }
        ]
    )
    return response.content[0].text