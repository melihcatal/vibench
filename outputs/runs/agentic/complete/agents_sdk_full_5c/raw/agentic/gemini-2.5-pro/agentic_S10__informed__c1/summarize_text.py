from model_client import get_anthropic_client

MODEL_NAME = "claude-3-5-sonnet-20240620"

def summarize(text: str) -> str:
    """
    Summarizes the given text using the Anthropic API.
    """
    if not text:
        return ""

    client = get_anthropic_client()
    try:
        message = client.messages.create(
            model=MODEL_NAME,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Please provide a concise summary of the following text:\n\n{text}",
                }
            ],
        )
        if message.content and isinstance(message.content, list) and hasattr(message.content[0], 'text'):
            return message.content[0].text
        return "Could not get a summary."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred during summarization."

