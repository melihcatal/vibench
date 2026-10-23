import os
import google.generativeai as genai

def summarize_meeting_chunk(transcript_chunk: str, model_name: str = "gemini-pro") -> str:
    """Summarizes a chunk of live meeting transcript using the Google Gemini API.

    Args:
        transcript_chunk (str): A segment of the meeting transcript to summarize.
        model_name (str): The name of the Gemini model to use (e.g., "gemini-pro").

    Returns:
        str: A concise summary of the transcript chunk.

    Raises:
        Exception: If the API call fails or the GOOGLE_API_KEY is not set.
    """
    # Ensure GOOGLE_API_KEY environment variable is set
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)

    try:
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""Summarize the following meeting transcript chunk concisely:

        Transcript Chunk:
        {transcript_chunk}

        Summary:"""

        response = model.generate_content(prompt)
        
        summary = response.text.strip()
        print(f"--- Transcript Chunk ---")
        print(transcript_chunk)
        print(f"--- Summary ---")
        print(summary)
        return summary

    except Exception as e:
        print(f"Error summarizing with Gemini API: {e}")
        return f"[Error summarizing chunk: {e}]"

if __name__ == "__main__":
    # To run this, ensure GOOGLE_API_KEY is set.
    # export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    print("Meeting summary using Google Gemini API.")

    dummy_transcript_chunk_1 = """
    The team discussed the Q3 marketing strategy. Sarah presented the social media campaign results, 
    showing a 15% engagement increase. Mark suggested focusing more on influencer collaborations 
    for the next quarter. John brought up budget concerns, which will be reviewed in the next meeting. 
    Action item: Sarah to draft a proposal for influencer outreach.
    """

    dummy_transcript_chunk_2 = """
    The technical team provided an update on the backend migration. The database transfer is 80% complete, 
    and they anticipate finishing by end of week. There was a minor hiccup with API integration, 
    but a workaround was found. Next steps involve rigorous testing of the new environment.
    """

    try:
        print("\n--- Summarizing Chunk 1 ---")
        summary_1 = summarize_meeting_chunk(dummy_transcript_chunk_1)
        print("\n--- Summarizing Chunk 2 ---")
        summary_2 = summarize_meeting_chunk(dummy_transcript_chunk_2)

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("Ensure GOOGLE_API_KEY is set for execution.")
