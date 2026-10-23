from model_client import get_openai_client
from model_models import ChatMessage

def summarize_text(text: str, model_id: str = "gpt-4o") -> str:
    client = get_openai_client()
    messages = [
        ChatMessage(role="system", content="You are a helpful assistant that summarizes text concisely."),
        ChatMessage(role="user", content=f"Please summarize the following text:
\n{text}")
    ]
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[m.to_dict() for m in messages],
            max_tokens=200,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error summarizing text: {e}"
