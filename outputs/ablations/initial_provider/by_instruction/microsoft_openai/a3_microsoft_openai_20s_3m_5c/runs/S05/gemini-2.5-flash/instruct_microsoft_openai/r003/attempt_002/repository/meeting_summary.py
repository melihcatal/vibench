import os
from anthropic import Anthropic

anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def summarize_meeting_chunk(transcript_chunk: str) -> str:
    try:
        response = anthropic_client.messages.create(
            model="claude-3-opus-20240229", # Using a specific Claude model
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": f"Please summarize the following meeting transcript chunk:
\n{transcript_chunk}"
                }
            ]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error summarizing: {e}"

if __name__ == "__main__":
    # Example usage
    sample_transcript = (
        "Participant A: So, we discussed the Q3 results and they look promising. "
        "Sales are up by 15% year-over-year. "
        "Participant B: That's great news! What about the new marketing campaign? "
        "Participant A: The new campaign launched last week and we're already seeing increased engagement. "
        "We expect it to contribute significantly to Q4."
    )
    summary = summarize_meeting_chunk(sample_transcript)
    print(f"Original Transcript Chunk:\n{sample_transcript}\n")
    print(f"Summary:\n{summary}")
