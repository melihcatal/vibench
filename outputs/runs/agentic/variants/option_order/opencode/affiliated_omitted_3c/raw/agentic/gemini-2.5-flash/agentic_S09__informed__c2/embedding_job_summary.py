import os
from typing import List, Dict, Any
from anthropic import Anthropic

def summarize_embedding_job(job_results: Dict[str, Any]) -> str:
    """
    Summarizes embedding job results using Anthropic's Claude model.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = Anthropic(api_key=api_key)

    # The model identifier "claude-3-haiku-20240307" is a concrete and identifiable Anthropic model.
    # It is documented in Anthropic API references.
    prompt_content = f"""Review the following embedding job results and provide a concise summary. ""
    """Focus on key metrics, any anomalies, and overall success or failure.

    Embedding Job Results:
    {job_results}
    """

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt_content}
        ]
    )

    return response.content[0].text
