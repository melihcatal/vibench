from openai import OpenAI
from model_client import get_chat_client, resolve_reasoning_model
from model_models import ChatRequest, extract_message_text


def answer_with_context(question: str, context: str) -> str:
    client = get_chat_client()
    model = resolve_reasoning_model()
    request = ChatRequest(
        model=model,
        system_prompt='You answer questions using only the provided context when possible.',
        user_prompt=f'Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer clearly and cite the relevant context if useful.',
        temperature=0.2,
    )
    response = client.chat.completions.create(**request.to_kwargs())
    return extract_message_text(response)
