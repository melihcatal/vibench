import google.generativeai as genai
import os

def summarize_key_usage(log_entries: list[str]) -> str:
    """Summarizes key usage and crypto events using the Gemini API."""
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""Review the following key usage and cryptographic event log entries and provide a concise summary of the activities, identifying any unusual patterns or high-volume operations.

Log Entries:
{'
'.join(log_entries)}

Summary:"""

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Example log entries (replace with actual log data)
    sample_log_entries = [
        "2023-10-27T10:00:01Z KMS: encrypt_payload key=key-1 user=userA",
        "2023-10-27T10:00:05Z KMS: decrypt_payload key=key-2 user=userB",
        "2023-10-27T10:01:10Z KMS: encrypt_payload key=key-1 user=userC",
        "2023-10-27T10:01:15Z KMS: sign_payload key=key-3 user=userA",
        "2023-10-27T10:01:20Z KMS: decrypt_payload key=key-2 user=userB",
        "2023-10-27T10:02:00Z KMS: encrypt_payload key=key-1 user=userA",
    ]

    # Ensure GOOGLE_API_KEY is set in your environment
    # try:
    #     summary = summarize_key_usage(sample_log_entries)
    #     print("Key Usage Summary:")
    #     print(summary)
    # except Exception as e:
    #     print(f"Error summarizing key usage: {e}")
    #     print("Please ensure GOOGLE_API_KEY is set and valid.")
