import os
import google.generativeai as genai

def summarize_transcript(transcript_text: str) -> str | None:
    """Summarizes a transcript using the Google Gemini Pro model."""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=google_api_key)

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Please provide a concise summary of the following transcript:

{transcript_text}

Summary:"

    try:
        print("Generating summary using Gemini Pro...")
        response = model.generate_content(prompt)
        summary = response.text
        print("Summary generated.")
        return summary
    except Exception as e:
        print(f"Error generating summary with Gemini Pro: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_API_KEY is set in your environment
    sample_long_transcript = (
        "This is a very long transcript of a meeting where we discussed various topics. "
        "First, we talked about the quarterly financial results, which were positive. "
        "Then, we moved on to the marketing strategy for the new product launch. "
        "There was some debate about the budget allocation for digital campaigns. "
        "Finally, we reviewed the upcoming team-building event and decided on a date. "
        "Everyone agreed that good communication is key to our success."
    )
    # summary = summarize_transcript(sample_long_transcript)
    # if summary:
    #     print("\nGenerated Summary:")
    #     print(summary)
    pass
