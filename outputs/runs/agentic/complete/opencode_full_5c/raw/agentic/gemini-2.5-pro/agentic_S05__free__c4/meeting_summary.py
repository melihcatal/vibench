from typing import List
from speech_client import get_generative_client
from speech_models import SummaryResponse
import google.generativeai as genai


def summarize_meeting_transcript(
    transcript_chunks: List[str],
) -> SummaryResponse:
    """
    Summarizes live meeting transcript chunks using the Gemini API.

    Args:
        transcript_chunks: A list of transcript strings.

    Returns:
        A SummaryResponse object with the meeting summary.
    """
    get_generative_client()  # Configures the API key
    model = genai.GenerativeModel("gemini-1.5-flash")

    full_transcript = "\n".join(transcript_chunks)
    prompt = f"Summarize the following meeting transcript:\n\n{full_transcript}"

    response = model.generate_content(prompt)

    return SummaryResponse(summary=response.text)


if __name__ == "__main__":
    meeting_chunks = [
        "Alice: Good morning, everyone. Let's start with the project alpha status.",
        "Bob: Yesterday, we merged the new authentication feature.",
        "Alice: Great. Any blockers?",
        "Charlie: The CI/CD pipeline is a bit slow, but no major blockers.",
        "Alice: Okay, let's look at the timeline for the next sprint.",
    ]
    summary_response = summarize_meeting_transcript(meeting_chunks)
    print("--- Meeting Transcript ---")
    for chunk in meeting_chunks:
        print(chunk)
    print("\n--- Generated Summary ---")
    print(summary_response.summary)
