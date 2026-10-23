import os
import anthropic

def summarize_transcript(transcript_text: str) -> str:
    """
    Summarizes a long transcript using the Anthropic Claude API.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
        
    client = anthropic.Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=512,
        temperature=0.0,
        system="You are a helpful assistant that summarizes meeting transcripts.",
        messages=[
            {
                "role": "user",
                "content": f"Please provide a concise summary of the following transcript:\n\n{transcript_text}"
            }
        ]
    )
    
    summary = message.content[0].text if message.content else "No summary generated."
    return summary
