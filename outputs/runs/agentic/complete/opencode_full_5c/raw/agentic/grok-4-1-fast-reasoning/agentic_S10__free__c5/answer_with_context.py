from model_client import openai_client
from model_models import parse_openai_chat


def answer_with_context(context: str, question: str) -> str:
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Answer the question based only on the provided context. If the answer is not in the context, say 'Information not available in context'.",
            },
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        temperature=0.1,
    )
    return parse_openai_chat(response)
