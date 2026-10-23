import os
import anthropic


def summarize_job(
    total_embeddings: int, failed_embeddings: int, duration_seconds: float
) -> str:
    """
    Summarizes the results of an embedding job using the Anthropic API.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""
Summarize the following embedding job result in a single paragraph:
- Total texts processed: {total_embeddings}
- Failed embeddings: {failed_embeddings}
- Total duration: {duration_seconds:.2f} seconds
"""

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    return message.content[0].text
