import os
from openai import OpenAI
from typing import List, Dict, Any


def summarize_error_logs(error_logs: List[Dict[str, Any]]) -> str:
    """
    Summarizes error log findings for incident review using OpenAI.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    prompt_content = (
        "The following is a list of JSON error logs from a recent incident. "
        "Please summarize the key findings, identify patterns, and suggest potential root causes.\n\n"
    )

    for log in error_logs:
        prompt_content += str(log) + "\n"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert system reliability engineer.",
                },
                {"role": "user", "content": prompt_content},
            ],
            temperature=0.5,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred while generating the summary: {e}"


if __name__ == "__main__":
    # Example usage with dummy data
    sample_errors = [
        {
            "timestamp": "2023-10-27T10:00:00Z",
            "severity": "ERROR",
            "payload": {
                "message": "Database connection failed: timeout",
                "service": "auth-service",
            },
        },
        {
            "timestamp": "2023-10-27T10:00:05Z",
            "severity": "ERROR",
            "payload": {
                "message": "Database connection failed: timeout",
                "service": "auth-service",
            },
        },
        {
            "timestamp": "2023-10-27T10:01:10Z",
            "severity": "ERROR",
            "payload": {
                "message": "Null pointer exception at user login",
                "service": "user-service",
                "traceId": "abc-123",
            },
        },
        {
            "timestamp": "2023-10-27T10:02:00Z",
            "severity": "ERROR",
            "payload": {
                "message": "Failed to write to cache",
                "service": "cache-service",
            },
        },
    ]
    summary = summarize_error_logs(sample_errors)
    print("--- Incident Summary ---")
    print(summary)
