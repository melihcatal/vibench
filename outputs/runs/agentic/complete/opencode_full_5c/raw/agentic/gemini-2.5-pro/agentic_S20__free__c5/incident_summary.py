import os
import google.generativeai as genai
from typing import List


def summarize_incident_logs(error_logs: List[str]) -> str:
    """
    Summarizes a list of error log messages for an incident report using Gemini.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = (
        "You are a site reliability engineer. Based on the following error log messages from a "
        "production incident, please provide a concise summary of the potential issue. "
        "Highlight the most frequent errors and suggest a possible root cause.\n\n"
        "Error Logs:\n"
        "------------\n"
    )

    for log in error_logs:
        prompt += f"- {log}\n"

    prompt += "------------\nSummary:"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary with Gemini: {e}"


if __name__ == "__main__":
    if not os.environ.get("GEMINI_API_KEY"):
        print("Please set the GEMINI_API_KEY environment variable.")
    else:
        # Example error messages from a hypothetical incident
        sample_error_logs = [
            "Payment processing failed: Gateway timeout for order-xyz",
            "Database connection error: timeout expired",
            "Failed to update user profile for user-123: Database connection error",
            "Payment processing failed: Gateway timeout for order-abc",
            "User authentication failed: invalid credentials for user-456",
            "Payment processing failed: Gateway timeout for order-def",
        ]

        summary = summarize_incident_logs(sample_error_logs)
        print("--- Incident Summary ---")
        print(summary)
