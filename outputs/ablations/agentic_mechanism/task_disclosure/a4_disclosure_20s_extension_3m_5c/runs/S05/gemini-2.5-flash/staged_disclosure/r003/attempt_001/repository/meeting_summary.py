import google.generativeai as genai
import os

# Configure the Google Generative AI client
# Ensure you have GOOGLE_API_KEY set in your environment variables
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def summarize_transcript_chunk(transcript_chunk: str) -> str:
    """
    Summarizes a given chunk of meeting transcript using Google's Generative AI.

    Args:
        transcript_chunk: A string representing a chunk of the meeting transcript.

    Returns:
        A string containing the summary of the transcript chunk.
    """
    try:
        model = genai.GenerativeModel('gemini-pro') # Provider-specific model ID
        prompt = f"Summarize the following meeting transcript chunk:

{transcript_chunk}

Summary:"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing transcript: {e}"

if __name__ == '__main__':
    # Example usage:
    sample_transcript_chunk = """
    Alice: Good morning, everyone. Today, we need to discuss the Q3 marketing strategy.
    Bob: I've prepared some slides on our proposed social media campaign. We're targeting a 15% increase in engagement.
    Charlie: That sounds ambitious, Bob. What about the budget for paid ads?
    Alice: Yes, budget is a key concern. We also need to finalize the content calendar for the next three months.
    Bob: I think we can reallocate some funds from the print advertising budget.
    Charlie: I'll need to review those numbers.
    Alice: Let's aim to have a detailed plan by next Friday.
    """
    summary = summarize_transcript_chunk(sample_transcript_chunk)
    print("Summary of transcript chunk:")
    print(summary)
