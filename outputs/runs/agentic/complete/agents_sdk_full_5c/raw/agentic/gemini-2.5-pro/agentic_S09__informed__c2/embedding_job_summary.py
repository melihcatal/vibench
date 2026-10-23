import os
import anthropic

def summarize_job_results(job_stats: str) -> str:
    """
    Summarizes embedding job results using Anthropic's Claude.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""
    Here are the statistics from a text embedding job. Please provide a brief,
    human-readable summary of the results.

    Job Statistics:
    {job_stats}

    Summary:
    """

    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=200,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        summary = message.content[0].text
        return summary
    except Exception as e:
        return f"Error generating summary: {e}"
