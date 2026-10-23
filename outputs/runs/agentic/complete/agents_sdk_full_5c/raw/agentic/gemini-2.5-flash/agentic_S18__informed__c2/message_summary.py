import google.generativeai as genai
import os

def summarize_message_results(results_text: str) -> str:
    """Summarizes message processing results using the Google Gemini API."""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for text summarization

    prompt = f"Please provide a concise summary of the following message processing results:\n\n{results_text}\n\nSummary:"

    try:
        response = model.generate_content(prompt)
        summary = response.text
        print(f"Summary generated: {summary}")
        return summary
    except Exception as e:
        print(f"Error summarizing with Gemini API: {e}")
        raise

if __name__ == "__main__":
    # Example usage with some dummy results
    sample_results = """
    Message 1001 processed successfully.
    Message 1002 failed with error: Invalid payload.
    Message 1003 processed successfully.
    Message 1004 processed successfully.
    Message 1005 failed with error: Database connection lost.
    """

    if not os.getenv("GOOGLE_API_KEY"):
        print("Please set the GOOGLE_API_KEY environment variable.")
    else:
        print("\n--- Summarizing sample message results ---")
        summarize_message_results(sample_results)
