from model_client import get_model_client
from model_models import ChatMessage

def summarize_text(text_to_summarize: str) -> str:
    """
    Summarizes the given text using an OpenAI model.
    """
    client = get_model_client()
    
    messages = [
        ChatMessage(role="system", content="You are a helpful assistant that summarizes text."),
        ChatMessage(role="user", content=f"Please summarize the following text:\n\n{text_to_summarize}")
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[m.to_dict() for m in messages],
            max_tokens=150,
            temperature=0.5,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        # In a real app, log this error
        print(f"An error occurred: {e}")
        return "An error occurred during summarization."
