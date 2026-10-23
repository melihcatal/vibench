import os
import anthropic

def summarize_transcript_chunk(transcript: str) -> str:
    """
    Summarizes a chunk of a live meeting transcript using Anthropic's Claude API.
    
    Requires the ANTHROPIC_API_KEY environment variable to be set.

    Args:
        transcript: A string containing a portion of the meeting transcript.

    Returns:
        A summary of the transcript chunk.
    """
    client = anthropic.Anthropic(
        # The client automatically reads the ANTHROPIC_API_KEY from env vars.
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

    prompt = f"""Human: Please summarize the following meeting transcript chunk concisely.
<transcript>
{transcript}
</transcript>

Assistant:"""

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    
    summary = message.content[0].text
    return summary
