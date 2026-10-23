import os
import sys
import google.generativeai as genai
from typing import List


def summarize_transcript(full_transcript_text: str) -> str:
    """
    Summarizes a given transcript using Google Generative AI (Gemini Pro).

    Args:
        full_transcript_text: The complete text of the transcript to summarize.

    Returns:
        A concise summary of the transcript.
    """
    # Ensure GOOGLE_API_KEY environment variable is set
    # For example: export GOOGLE_API_KEY="your-api-key"
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")  # Using Gemini Pro for summarization

    prompt = f"Please provide a concise summary of the following meeting transcript:\n\n{full_transcript_text}\n\nSummary:"

    print("Generating summary using Google Generative AI (Gemini Pro)...")
    # The actual summarization happens here
    response = model.generate_content(prompt)
    summary = response.text.strip()

    print(f"Generated Summary:\n{summary}")
    return summary


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python archive_summary.py <path_to_transcript_file>")
        print("Example: python archive_summary.py my_meeting_transcript.txt")
        sys.exit(1)

    transcript_file_path = sys.argv[1]

    if not os.path.exists(transcript_file_path):
        print(f"Error: Transcript file not found at {transcript_file_path}")
        sys.exit(1)

    with open(transcript_file_path, "r") as f:
        full_transcript = f.read()

    try:
        summary = summarize_transcript(full_transcript)
        print("\n--- Summarization Complete ---")
        print(summary)
    except Exception as e:
        print(f"Error summarizing transcript: {e}")
        sys.exit(1)
