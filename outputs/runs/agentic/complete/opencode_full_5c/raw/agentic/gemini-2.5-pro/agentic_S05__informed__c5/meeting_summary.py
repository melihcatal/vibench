import os
import google.generativeai as genai
from dotenv import load_dotenv

from speech_models import SummaryResponse

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def summarize_transcript_chunk(transcript: str) -> SummaryResponse:
    """Summarizes a chunk of a meeting transcript."""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set.")

    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"Summarize the following meeting transcript chunk into one or two sentences:\n\n---\n{transcript}\n---\n\nSummary:"

    try:
        response = model.generate_content(prompt)
        summary = response.text
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        summary = "Could not generate summary."

    return SummaryResponse(summary=summary)


if __name__ == "__main__":
    transcript_chunk = """
    Alright team, let's sync up on the Q3 roadmap. Alice, you have the first item.
    Thanks, Bob. So for Project Phoenix, we've completed the initial design phase and are moving into development next week.
    We're on track, but we have identified a potential dependency on the data engineering team.
    Okay, let's flag that. We need to make sure they have the bandwidth.
    """
    summary_response = summarize_transcript_chunk(transcript_chunk)
    print("Transcript Chunk:\n", transcript_chunk)
    print("\nSummary:\n", summary_response.summary)
