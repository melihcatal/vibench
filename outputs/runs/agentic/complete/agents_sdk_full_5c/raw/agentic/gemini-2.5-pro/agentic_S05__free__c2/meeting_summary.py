import os
import cohere

def summarize_meeting_chunk(transcript_chunk: str) -> dict:
    """
    Summarizes a chunk of a live meeting transcript using the Cohere API.

    Args:
        transcript_chunk: A string containing a portion of the meeting transcript.

    Returns:
        A dictionary containing the summary or an error.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        return {"error": "COHERE_API_KEY environment variable not set."}

    try:
        co = cohere.Client(api_key)
        response = co.summarize(
            text=transcript_chunk,
            model='command',
            length='short',
            extractiveness='medium'
        )
        return {
            "original_chunk": transcript_chunk,
            "summary": response.summary
        }
    except Exception as e:
        print(f"An error occurred with the Cohere API: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    meeting_text = (
        "Alright team, let's kick off the weekly sync. First on the agenda is a review of the Q3 roadmap. "
        "We've seen some great progress on the Alpha project, but the Beta project is lagging behind schedule. "
        "We need to re-allocate resources to get it back on track. Any thoughts on how to do that? "
        "Also, marketing has a new campaign they want to launch next month, which will impact our current sprint."
    )
    
    if os.getenv("COHERE_API_KEY"):
        summary_result = summarize_meeting_chunk(meeting_text)
        if "summary" in summary_result:
            print("--- Original Text ---")
            print(summary_result["original_chunk"])
            print("\n--- Summary ---")
            print(summary_result["summary"])
    else:
        print("COHERE_API_KEY not set. Skipping summarization example.")
