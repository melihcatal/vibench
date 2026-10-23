from model_client import get_openai_client
from model_models import Message


def summarize_text(text_to_summarize: str) -> str:
    client = get_openai_client()

    messages = [
        Message(
            role="system", content="You are a helpful assistant that summarizes text."
        ),
        Message(
            role="user",
            content=f"Please summarize the following text:\n\n{text_to_summarize}",
        ),
    ]

    chat_completion = client.chat.completions.create(
        messages=[msg.dict() for msg in messages],
        model="gpt-4o",
    )

    if chat_completion.choices:
        return chat_completion.choices[0].message.content
    return ""
