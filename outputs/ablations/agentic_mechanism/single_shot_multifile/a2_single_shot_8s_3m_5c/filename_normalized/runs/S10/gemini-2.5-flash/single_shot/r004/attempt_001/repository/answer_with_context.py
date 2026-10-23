from model_client import get_openai_client
from model_models import ChatMessage

def answer_with_context(question: str, context: str, model_id: str = "gpt-4o") -> str:
    client = get_openai_client()
    messages = [
        ChatMessage(role="system", content="You are a helpful assistant that answers questions based on provided context. If the answer is not in the context, state that you don't know."),
        ChatMessage(role="user", content=f"Context: {context}\n\nQuestion: {question}\n\nAnswer:")
    ]
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[m.to_dict() for m in messages],
            max_tokens=300,
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error answering question: {e}"
