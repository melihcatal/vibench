import os
import google.generativeai as genai

def summarize_rotation_status(rotation_log_entry: str) -> str:
    """
    Summarizes a secret rotation status using the Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following secret rotation log entry:

{rotation_log_entry}"

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Example usage (requires GOOGLE_API_KEY to be set)
    example_log = """
    Secret 'my-db-password' rotation initiated at 2023-10-27T10:00:00Z.
    Old version (v5) marked for destruction. New version (v6) created and activated.
    Applications 'backend-service' and 'data-pipeline' successfully updated to v6.
    Monitoring shows no errors post-rotation. Next rotation scheduled for 2024-01-27.
    """
    try:
        summary = summarize_rotation_status(example_log)
        print(f"Rotation Summary:\n{summary}")
    except Exception as e:
        print(f"Error summarizing rotation status: {e}")
