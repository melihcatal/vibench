import os
import google.generativeai as genai

def summarize_text_with_gemini(text_content: str, model_name: str = "gemini-pro") -> str:
    """
    Summarizes the given text using the Google Gemini API.

    Args:
        text_content: The text to summarize.
        model_name: The name of the Gemini model to use (e.g., "gemini-pro").

    Returns:
        The summarized text.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel(model_name)

    prompt = f"Please provide a concise summary of the following meeting transcript:

{text_content}

Summary:"

    response = model.generate_content(prompt)

    # Access the text from the first part of the first candidate
    return response.candidates[0].content.parts[0].text

def meeting_summary_generator(transcript_chunk: str) -> str:
    """
    Generates a summary for a chunk of meeting transcript.
    Requires GOOGLE_API_KEY environment variable to be set.
    """
    if not os.getenv("GOOGLE_API_KEY"):
        print("Please set GOOGLE_API_KEY environment variable for Gemini API.")
        return "[Summary Error: GOOGLE_API_KEY not set]"

    if not transcript_chunk.strip():
        return "[No content to summarize]"

    try:
        summary = summarize_text_with_gemini(transcript_chunk)
        return summary
    except Exception as e:
        print(f"Error generating meeting summary: {e}")
        return f"[Summary Generation Error: {e}]"

if __name__ == "__main__":
    # Set your GOOGLE_API_KEY environment variable
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"

    # example_transcript = (
    #     "The meeting started with a discussion about Q3 financial results. "
    #     "Sarah presented the sales figures, noting a 10% increase in revenue. "
    #     "John raised concerns about marketing spend efficiency. "
    #     "Action item: Sarah to investigate marketing ROI for Q3. "
    #     "Next, we discussed the new product launch. "
    #     "Mike outlined the timeline and key milestones. "
    #     "There was a brief debate about feature prioritization. "
    #     "Action item: Mike to finalize feature list by end of week. "
    #     "The meeting concluded with a reminder about the upcoming team-building event."
    # )

    # summary = meeting_summary_generator(example_transcript)
    # print(f"Original Transcript:\n{example_transcript}\n")
    # print(f"Meeting Summary:\n{summary}")

    # empty_transcript = ""
    # empty_summary = meeting_summary_generator(empty_transcript)
    # print(f"Empty Transcript Summary: {empty_summary}")
    pass
