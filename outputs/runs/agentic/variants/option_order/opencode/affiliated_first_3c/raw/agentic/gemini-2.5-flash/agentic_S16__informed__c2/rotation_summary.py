import google.generativeai as genai
import os
from typing import List, Dict, Any


def summarize_rotation_status(rotation_logs: List[Dict[str, Any]]) -> str:
    """Summarizes secret rotation status using the Google Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    log_summary = "\n".join(
        [
            f"- Secret: {log.get('secret_id')}, Status: {log.get('status')}, Last Rotated: {log.get('last_rotated')}"
            for log in rotation_logs
        ]
    )

    prompt = f"""Review the following secret rotation logs and provide a concise summary of the overall rotation status, highlighting any potential issues or successes.

Secret Rotation Logs:
{log_summary}

Summary:"""

    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    # Example usage
    sample_logs = [
        {"secret_id": "api-key-1", "status": "completed", "last_rotated": "2024-03-01"},
        {
            "secret_id": "db-password-prod",
            "status": "failed",
            "last_rotated": "2024-02-15",
        },
        {
            "secret_id": "json-config",
            "status": "completed",
            "last_rotated": "2024-03-10",
        },
        {
            "secret_id": "service-account-key",
            "status": "pending",
            "last_rotated": "2024-03-05",
        },
    ]

    # Ensure GOOGLE_API_KEY is set in environment variables
    if "GOOGLE_API_KEY" not in os.environ:
        print("Warning: GOOGLE_API_KEY environment variable not set. Using dummy key.")
        os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"

    summary = summarize_rotation_status(sample_logs)
    print("\n--- Rotation Summary ---")
    print(summary)
