import os
from openai import OpenAI

def summarize_transcript(transcript_text: str) -> str:
    """
    Summarizes a long transcript using the OpenAI API.

    Args:
        transcript_text: The full text of the transcript.

    Returns:
        A concise summary of the transcript.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant designed to summarize meeting transcripts. Provide a concise summary of the key points, decisions, and action items.",
                },
                {
                    "role": "user", 
                    "content": transcript_text
                },
            ],
            temperature=0.5,
            max_tokens=256,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "No summary could be generated."
    except Exception as e:
        print(f"An error occurred while summarizing: {e}")
        return "Error: Could not generate summary."

if __name__ == '__main__':
    sample_transcript = """
    Speaker A: Good morning, everyone. The main topic today is the Q3 marketing campaign. We need to finalize the budget.
    Speaker B: I've reviewed the proposal. The projected ad spend is too high. We need to reduce it by at least 15%.
    Speaker A: I agree. Let's re-allocate some of that budget to content creation. John, can you take the lead on that?
    Speaker C: I'm on it. I'll have a revised plan by end of day Friday.
    Speaker B: Perfect. So, the action item is for John to revise the content budget. Any other points?
    Speaker A: No, that's it for today. Let's adjourn.
    """
    
    summary = summarize_transcript(sample_transcript)
    print("Transcript Summary:")
    print(summary)
