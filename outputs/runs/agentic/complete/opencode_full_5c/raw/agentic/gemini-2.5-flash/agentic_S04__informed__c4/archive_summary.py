import os
import google.generativeai as genai

def summarize_transcript(transcript_text: str) -> str:
    """Summarizes transcription results using the Google Gemini API."""
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # Use a specific Gemini model for summarization
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Please summarize the following transcript:

{transcript_text}

Summary:"

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage
    # sample_transcript = "This is a long transcript about a meeting where we discussed the new product launch and marketing strategies. We also talked about the budget and timelines. The team agreed on next steps."
    # summary = summarize_transcript(sample_transcript)
    # print(f"Summary: {summary}")
    pass
