from model_client import get_client, MODEL_NAME
from model_models import make_messages, extract_content

def answer_with_context(question: str, context: str) -> str:
    client = get_client()
    messages = make_messages(
        "You answer questions accurately based solely on the provided context. If the answer is not in the context, respond 'Information not found in the provided context.'",
        f"Context: {context}\n\nQuestion: {question}"
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,
        max_tokens=500,
    )
    return extract_content(response)
