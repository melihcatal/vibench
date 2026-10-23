import google.generativeai as genai
import os

def initialize_gemini():
    """Initializes the Google Gemini API client."""
    if "GOOGLE_API_KEY" not in os.environ:
        print("Warning: GOOGLE_API_KEY environment variable not set.")
        print("Please set your GOOGLE_API_KEY to use the Gemini API.")
        return None
    
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    return genai.GenerativeModel('gemini-pro') # Using gemini-pro for text generation

def summarize_meeting_chunk(transcript_chunk: str, model: genai.GenerativeModel) -> str:
    """Summarizes a chunk of meeting transcript using the Google Gemini API.

    Args:
        transcript_chunk: A segment of the meeting transcript.
        model: An initialized Google Gemini GenerativeModel.

    Returns:
        A concise summary of the transcript chunk.
    """
    if not model:
        return "Error: Gemini model not initialized. Check GOOGLE_API_KEY."

    if not transcript_chunk.strip():
        return ""

    prompt = f"""Summarize the following meeting transcript chunk in one concise sentence:

{transcript_chunk}

Summary:"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error summarizing with Gemini API: {e}")
        return f"Error: Could not summarize content. {e}"

if __name__ == "__main__":
    print("Initializing Gemini model...")
    gemini_model = initialize_gemini()

    if gemini_model:
        print("\n--- Summarizing a sample transcript chunk ---")
        sample_transcript = (
            "The team discussed the Q3 sales performance. John presented the regional breakdown, "
            "highlighting strong growth in EMEA but a slight dip in APAC. Sarah suggested a new marketing "
            "campaign for APAC, focusing on local partnerships. The next steps involve John preparing a detailed "
            "report for the board meeting, and Sarah drafting a proposal for the APAC campaign strategy."
        )
        summary = summarize_meeting_chunk(sample_transcript, gemini_model)
        print(f"Original Transcript:\n{sample_transcript}\n")
        print(f"Summary:\n{summary}\n")

        print("\n--- Summarizing another chunk ---")
        another_transcript = (
            "The engineering team reviewed the sprint progress. Task #123 is 80% complete, "
            "but Task #456 is blocked by a dependency on the frontend team. Mark volunteered to "
            "coordinate with the frontend lead to unblock it. The team also decided to prioritize "
            "bug fixes for the next two days before resuming new feature development."
        )
        summary_2 = summarize_meeting_chunk(another_transcript, gemini_model)
        print(f"Original Transcript:\n{another_transcript}\n")
        print(f"Summary:\n{summary_2}\n")
    else:
        print("Gemini model not available. Skipping summary demonstration.")
