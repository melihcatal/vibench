import google.generativeai as genai
import os

# Configure the API key. Replace with your actual API key or set as environment variable.
# For production, it's recommended to use a secure method for API key management.
# For example: genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
genai.configure(api_key="YOUR_GEMINI_API_KEY")

def summarize_transcript_chunk(transcript_chunk: str) -> str:
    """Summarizes a chunk of live meeting transcript using Google's Gemini API.

    Args:
        transcript_chunk: A segment of the meeting transcript to summarize.

    Returns:
        A concise summary of the transcript chunk.
    """
    model = genai.GenerativeModel('gemini-pro') # Using a capable model for summarization

    prompt = f"Please summarize the following meeting transcript chunk concisely:\n\n{transcript_chunk}\n\nSummary:"

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error summarizing transcript: {e}")
        return ""
