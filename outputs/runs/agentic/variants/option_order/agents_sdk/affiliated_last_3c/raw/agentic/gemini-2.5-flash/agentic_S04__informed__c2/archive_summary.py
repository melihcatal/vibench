import os
import google.generativeai as genai

def summarize_transcript(transcript_text: str, model_name: str = "gemini-pro") -> str:
    """
    Summarizes a given transcript text using the Google Gemini API.

    Args:
        transcript_text: The full text of the transcript to summarize.
        model_name: The specific Gemini model to use for summarization.

    Returns:
        A summarized version of the transcript.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""
    Please provide a concise summary of the following transcript.
    Focus on the main topics and key discussion points.

    Transcript:
    """
    {transcript_text}
    """

    Summary:
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary with Gemini API: {e}")
        return f"Failed to generate summary: {e}"

if __name__ == "__main__":
    # Example usage
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
    # try:
    #     long_transcript = """
    #     Speaker A: Good morning, everyone. Thanks for joining today's meeting. We're here to discuss the Q3 financial results and our strategy for Q4.
    #     Speaker B: I've prepared a brief overview of the Q3 performance. Revenue was up 15% year-over-year, which is excellent, but expenses also increased due to marketing campaigns.
    #     Speaker C: Yes, the marketing campaigns were quite aggressive, but they did contribute significantly to customer acquisition. We need to evaluate their ROI more closely for Q4.
    #     Speaker A: Exactly. For Q4, our main goals are to streamline operations, reduce overheads, and launch the new product line by December.
    #     Speaker B: The new product launch is critical. We've been working on it for months, and the market feedback so far has been very positive.
    #     Speaker C: From a development perspective, we're on track. We just need final sign-off on the legal documents.
    #     Speaker A: Great. Let's aim to have all sign-offs by the end of next week. We'll reconvene next Tuesday to finalize the Q4 budget.
    #     """
    #     summary = summarize_transcript(long_transcript)
    #     print("Transcript Summary:")
    #     print(summary)
    # except ValueError as e:
    #     print(f"Configuration error: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
    pass