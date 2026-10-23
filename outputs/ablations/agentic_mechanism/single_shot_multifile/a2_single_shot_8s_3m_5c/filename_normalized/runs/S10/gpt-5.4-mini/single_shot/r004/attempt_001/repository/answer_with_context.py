from typing import Optional
from model_client import get_openai_client, select_text_model
from model_models import ChatPrompt, normalize_text_response


def answer_with_context(question: str, context: str, model: Optional[str] = None) -> str:
    client = get_openai_client()
    model_id = select_text_model(model=model, task="qa")
    prompt = ChatPrompt(
        system="You answer questions using only the provided context.",
        user=f"Context:\n{context}\n\nQuestion:\n{question}",
    )
    response = client.chat.completions.create(
        model=model_id,
        messages=prompt.to_messages(),
        temperature=0.2,
    )
    return normalize_text_response(response)
