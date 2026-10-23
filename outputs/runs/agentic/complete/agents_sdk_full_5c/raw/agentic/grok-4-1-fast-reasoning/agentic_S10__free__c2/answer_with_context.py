from model_client import client
from model_models import extract_completion_content

def answer_with_context(question: str, context: str) -> str:
    messages = [
        {"role": "system", "content": "Answer the question based only on the provided context. If the answer is not in the context, say 'I don't know'."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.1,
    )
    return extract_completion_content(response)