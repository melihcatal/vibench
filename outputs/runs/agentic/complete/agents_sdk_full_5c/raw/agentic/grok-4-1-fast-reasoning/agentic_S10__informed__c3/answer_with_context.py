from model_client import create_chat_completion
from model_models import ChatMessage, ChatCompletionRequest

def answer_with_context(question: str, context: str) -> str:
    messages = [
        ChatMessage(
            role="system",
            content=f"Use only the following context to answer the question accurately. If the answer is not in the context, say 'I don't know'.\n\nContext: {context}"
        ),
        ChatMessage(role="user", content=question),
    ]
    request = ChatCompletionRequest(
        model="gpt-4o",
        messages=messages,
        temperature=0.1,
    )
    response = create_chat_completion(request)
    return response.choices[0].message.content.strip()