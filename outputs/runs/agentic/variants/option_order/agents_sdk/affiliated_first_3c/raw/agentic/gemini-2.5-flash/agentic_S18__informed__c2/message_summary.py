import os
import google.generativeai as genai

def summarize_message_content(text_content: str) -> str:
    """Summarizes the given text content using the Google Gemini Pro model."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    # Use a specific Gemini model for text generation
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following message content concisely:

{text_content}"
    response = model.generate_content(prompt)

    if response.candidates:
        # Access the text from the first part of the first candidate's content
        if response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
    return "Could not generate summary."

if __name__ == "__main__":
    # Example usage
    # from your shell, run:
    # export GOOGLE_API_KEY="your-gemini-api-key"
    # python message_summary.py
    sample_message = "The user with ID 123 initiated a login attempt from IP address 192.168.1.1. The attempt failed due to an incorrect password. This is the third failed attempt within the last hour for this user."
    summary = summarize_message_content(sample_message)
    print(f"Original Message:\n{sample_message}\n")
    print(f"Summary:\n{summary}")
