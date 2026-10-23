import os
import anthropic

# Provider: Anthropic
# SDK: anthropic

def summarize_content(text_content: str, max_tokens: int = 512) -> str | None:
    """
    Summarizes the provided text content using the Anthropic Claude API.
    Requires ANTHROPIC_API_KEY environment variable.

    :param text_content: The text content to summarize.
    :param max_tokens: The maximum number of tokens for the summary.
    :return: The summarized text, or None on failure.
    """
    try:
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": f"Please summarize the following document:\n\n{text_content}",
                }
            ],
        )
        return message.content[0].text
    except Exception as e:
        print(f"An error occurred during summarization with Anthropic: {e}")
        return None
