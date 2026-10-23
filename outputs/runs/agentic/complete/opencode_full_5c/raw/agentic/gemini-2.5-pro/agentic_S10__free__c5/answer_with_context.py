from model_client import get_model_client
from model_models import CompletionResponse


def answer_with_context(question: str, context: str) -> CompletionResponse:
    client = get_model_client()
    prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on the provided context.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    answer = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason
    return CompletionResponse(text=answer, finish_reason=finish_reason)
