from model_client import create_chat_completion
from model_models import ChatMessage, ChatCompletionRequest

def summarize_text(text: str) -> str:
    messages = [
        ChatMessage(role="system", content="You are an expert summarizer. Provide a concise and accurate summary of the given text."),
        ChatMessage(role="user", content=text),
    ]
    request = ChatCompletionRequest(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
    )
    response = create_chat_completion(request)
    return response.choices[0].message.content.strip()