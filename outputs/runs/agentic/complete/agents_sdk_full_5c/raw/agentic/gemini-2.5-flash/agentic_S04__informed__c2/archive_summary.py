import os
import google.generativeai as genai
from speech_models import SummaryResult

def archive_summary(transcript_text: str) -> SummaryResult:
    """Summarizes transcription results using the Google Gemini API."""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # Use a specific Gemini model
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Please provide a concise summary of the following meeting transcript:\n\n{transcript_text}\n\nSummary:"

    response = model.generate_content(prompt)

    summary = response.text

    return SummaryResult(
        original_text=transcript_text,
        summary=summary
    )

if __name__ == "__main__":
    # Example usage (requires GOOGLE_API_KEY environment variable)
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"
    # 
    # try:
    #     example_transcript = """
    #     Speaker 1: Good morning team, let's start with the project update.
    #     Speaker 2: The frontend development is on track, no major blockers.
    #     Speaker 1: Great. How about the backend, John?
    #     Speaker 3: Backend is facing some integration issues with the new payment gateway, but we expect to resolve it by end of day.
    #     Speaker 1: Okay, please keep me posted. We need to aim for a release next week.
    #     Speaker 2: Understood.
    #     """
    #     summary_result = archive_summary(example_transcript)
    #     print(f"Original Transcript:\n{summary_result.original_text}")
    #     print(f"\nGenerated Summary:\n{summary_result.summary}")
    # except Exception as e:
    #     print(f"Error summarizing: {e}")
    pass
