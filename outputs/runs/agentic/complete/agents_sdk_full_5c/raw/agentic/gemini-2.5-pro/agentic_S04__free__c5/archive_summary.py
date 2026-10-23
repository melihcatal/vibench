import os
import anthropic

def summarize_transcript_for_archive(full_transcript: str) -> str:
    """
    Summarizes a full transcript using Anthropic's Claude model.

    Args:
        full_transcript: The complete text of the transcription.

    Returns:
        A concise summary of the transcript.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": f"Please provide a concise summary of the following meeting transcript:\n\n{full_transcript}"
            }
        ]
    )
    
    return message.content[0].text
