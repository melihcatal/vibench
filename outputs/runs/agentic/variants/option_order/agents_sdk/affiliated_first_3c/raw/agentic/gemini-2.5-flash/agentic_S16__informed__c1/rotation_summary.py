import google.generativeai as genai
import os

def summarize_rotation_notes(runbook_notes: str) -> str:
    """
    Summarizes secret rotation runbook notes using the Google Gemini API.
    Requires GOOGLE_API_KEY environment variable.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following secret rotation runbook notes concisely, highlighting key actions and dates:\n\n{runbook_notes}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API for summarization: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    # os.environ['GOOGLE_API_KEY'] = 'YOUR_GEMINI_API_KEY'
    sample_notes = """
    Runbook for API Key Rotation (Service A)
    1. On 2023-01-15, generated new API key in AWS Secrets Manager.
    2. Updated all dependent services (Service X, Service Y) to use the new key by 2023-01-16.
    3. Old key marked for deprecation on 2023-01-17.
    4. Scheduled old key deletion for 2023-02-01.
    5. Verified successful rotation by monitoring logs of Service X and Y.
    Next rotation due: 2024-01-15.
    """
    try:
        summary = summarize_rotation_notes(sample_notes)
        print("Rotation Summary:")
        print(summary)
    except Exception:
        print("Failed to summarize rotation notes.")
