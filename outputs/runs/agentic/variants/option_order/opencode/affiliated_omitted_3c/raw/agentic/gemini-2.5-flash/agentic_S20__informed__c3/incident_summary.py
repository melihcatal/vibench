import os
from openai import OpenAI
from typing import List


def summarize_error_logs_for_incident(
    error_logs: List[str], model: str = "gpt-3.5-turbo"
) -> str:
    """Summarizes a list of error log messages for incident review using OpenAI's chat completions.

    Args:
        error_logs: A list of error log message strings.
        model: The OpenAI model to use for summarization (default: gpt-3.5-turbo).

    Returns:
        A summarized incident report.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    log_string = "\n".join(error_logs)
    prompt = (
        "Summarize the following error logs for an incident review. "
        "Identify key issues, potential causes, and frequency of errors.\n\n"
        f"Logs:\n{log_string}"
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that summarizes error logs.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error summarizing logs: {e}"
