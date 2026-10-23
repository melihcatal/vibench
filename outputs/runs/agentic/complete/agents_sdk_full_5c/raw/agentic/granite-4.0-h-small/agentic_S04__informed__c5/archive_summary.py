# [LATER-STEP] archive_summary.py
# Summarize transcription results using Gemini API (hosted LLM inference)

import os
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=GOOGLE_API_KEY)

def archive_summary(transcript: str, summary_length: int = 150) -> str:
    """Generates a concise summary of the full transcript using Google Gemini.
    Returns the summary text.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(
        f"Summarize the following meeting transcript in {summary_length} words:\n\n{transcript}"
    )
    return response.text.strip()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: archive_summary.py <transcript_text> [summary_length]")
        sys.exit(1)
    transcript = sys.argv[1]
    length = int(sys.argv[2]) if len(sys.argv) > 2 else 150
    summary = archive_summary(transcript, length)
    print("Summary:")
    print(summary)
