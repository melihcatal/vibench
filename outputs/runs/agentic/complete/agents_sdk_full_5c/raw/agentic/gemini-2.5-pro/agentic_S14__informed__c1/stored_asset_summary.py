import os
import anthropic

def summarize_text_with_anthropic(text_content: str) -> str:
    """
    Summarizes text content using the Anthropic Claude API.

    Args:
        text_content (str): The text content to summarize.

    Returns:
        str: The summarized text.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Please provide a concise summary of the following document:\n\n{text_content}",
            }
        ],
    )
    
    summary = ""
    if message.content and isinstance(message.content[0], anthropic.types.TextBlock):
        summary = message.content[0].text
        
    return summary
