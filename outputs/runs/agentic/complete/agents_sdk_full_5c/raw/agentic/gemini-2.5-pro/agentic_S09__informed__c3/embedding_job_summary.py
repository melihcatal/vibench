import os
import anthropic

def summarize_job(texts_embedded: int, duration_seconds: float, model: str = "claude-3-sonnet-20240229") -> str:
    """
    Summarizes the results of an embedding job using the Anthropic API.

    Args:
        texts_embedded: The total number of texts that were embedded.
        duration_seconds: The duration of the job in seconds.
        model: The Anthropic model to use for summarization.

    Returns:
        A human-readable summary of the job.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""
        An text embedding job has completed. Please provide a brief, human-readable summary.

        Job Details:
        - Total texts embedded: {texts_embedded}
        - Job duration: {duration_seconds:.2f} seconds
        
        Summarize the key results.
        """

    message = client.messages.create(
        model=model,
        max_tokens=200,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text
