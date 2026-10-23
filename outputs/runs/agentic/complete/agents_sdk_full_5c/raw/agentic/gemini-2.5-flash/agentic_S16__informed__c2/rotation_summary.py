import os
import google.generativeai as genai

def summarize_rotation_status(rotation_logs: str) -> str:
    """
    Summarizes secret rotation status using the Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Summarize the following secret rotation logs, highlighting any failures or key events:

{rotation_logs}

Summary:"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing rotation status: {e}"

if __name__ == "__main__":
    # Set GOOGLE_API_KEY environment variable

    sample_logs = """
    [2023-10-26 10:00:01] INFO: Secret 'db-password' rotation initiated.
    [2023-10-26 10:00:05] INFO: New secret version created for 'db-password'.
    [2023-10-26 10:00:10] ERROR: Application 'backend-service' failed to update with new 'db-password'. Connection refused.
    [2023-10-26 10:00:15] INFO: Secret 'api-key' rotation initiated.
    [2023-10-26 10:00:20] INFO: Secret 'api-key' successfully rotated and applications updated.
    """

    if os.environ.get("GOOGLE_API_KEY"):
        print("Generating summary...")
        summary = summarize_rotation_status(sample_logs)
        print("\n--- Rotation Summary ---")
        print(summary)
    else:
        print("GOOGLE_API_KEY environment variable not set. Skipping summarization example.")
