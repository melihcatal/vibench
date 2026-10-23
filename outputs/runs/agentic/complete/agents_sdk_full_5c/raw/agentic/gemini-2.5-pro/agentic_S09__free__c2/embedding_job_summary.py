import os
import anthropic

def summarize_job(total_embeddings: int, time_taken_seconds: float) -> str:
    """
    Summarizes the results of an embedding job using Anthropic Claude.

    Args:
        total_embeddings: The number of embeddings created.
        time_taken_seconds: The time elapsed for the job.

    Returns:
        A human-readable summary.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""
Please provide a brief, human-readable summary for the following embedding job results:
- Total texts embedded: {total_embeddings}
- Total time taken: {time_taken_seconds:.2f} seconds

Focus on clarity and conciseness.
"""

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return message.content[0].text
