import os
import google.generativeai as genai

def summarize_transcript(text: str, model_name: str = "gemini-pro") -> str:
    """
    Summarizes the given transcript text using the Google Gemini API.

    Args:
        text: The transcript text to summarize.
        model_name: The name of the Gemini model to use for summarization (e.g., "gemini-pro").

    Returns:
        A summarized version of the transcript.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # Initialize the Generative Model
    model = genai.GenerativeModel(model_name)

    prompt = f"Please provide a concise summary of the following transcript:

{text}

Summary:"

    try:
        print(f"Generating summary using {model_name} for text (first 50 chars): {text[:50]}...")
        response = model.generate_content(prompt)
        
        if response.parts:
            summary = " ".join([part.text for part in response.parts])
            print("Summary generated.")
            return summary
        else:
            raise Exception("Gemini API did not return a summary.")

    except Exception as e:
        raise Exception(f"Error calling Gemini API for summarization: {e}")

if __name__ == "__main__":
    try:
        # Example usage: Ensure GOOGLE_API_KEY is set
        sample_transcript = (
            "The first speaker began the meeting by discussing the quarterly financial results. "
            "They highlighted a 15% increase in revenue compared to the previous quarter, "
            "attributing it to successful marketing campaigns and new product launches. "
            "The second speaker then raised concerns about operational costs, suggesting "
            "areas for potential reduction, particularly in supply chain logistics. "
            "A third speaker proposed an agenda item for the next meeting to deep-dive "
            "into cost-saving strategies. The meeting concluded with an agreement to "
            "circulate the financial report and schedule a follow-up discussion."
        )

        summary_result = summarize_transcript(sample_transcript)
        print("\n--- Generated Summary ---")
        print(summary_result)

    except Exception as e:
        print(f"Error in summarization: {e}")
