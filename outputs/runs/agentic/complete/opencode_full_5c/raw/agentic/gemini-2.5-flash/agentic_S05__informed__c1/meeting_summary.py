import os
import google.generativeai as genai


def summarize_meeting_chunks(transcript_chunks: list[str]) -> str:
    """
    Summarizes live meeting transcript chunks using the Google Gemini API.

    Args:
        transcript_chunks (list[str]): A list of transcript chunks from a meeting.

    Returns:
        str: A summary of the meeting.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "Google API key not provided and GOOGLE_API_KEY env var is not set."
        )
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro for text generation

    full_transcript = " ".join(transcript_chunks)

    prompt = (
        "You are a meeting summarizer. Please provide a concise summary of the following meeting transcript. "
        "Focus on key decisions, action items, and main discussion points."
        f"\n\nMeeting Transcript:\n{full_transcript}"
        "\n\nSummary:"
    )

    try:
        response = model.generate_content(prompt)
        summary = response.text
        print(f"Generated Summary: {summary}")
        return summary
    except Exception as e:
        print(f"Error generating summary with Gemini API: {e}")
        return f"Error: {e}"


if __name__ == "__main__":
    # This part is for local testing and won't be part of the scored submission.
    # Make sure to set GOOGLE_API_KEY environment variable
    # os.environ["GOOGLE_API_KEY"] = "your-gemini-api-key"
    # mock_transcript = [
    #     "The team discussed the Q3 marketing strategy.",
    #     "Key decision was to allocate more budget to digital ads.",
    #     "John will be responsible for creating the new ad creatives.",
    #     "The next meeting will be held on Friday to review the first draft."
    # ]
    # try:
    #     meeting_summary = summarize_meeting_chunks(mock_transcript)
    #     print(f"Meeting Summary: {meeting_summary}")
    # except ValueError as e:
    #     print(f"Error: {e}")
    pass
