from model_client import get_openai_client
from model_models import ModelResponse


def answer_with_context(question: str, context: str) -> ModelResponse:
    client = get_openai_client()
    prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on the provided context.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
        temperature=0.3,
    )
    choice = response.choices[0]
    return ModelResponse(
        text=choice.message.content,
        finish_reason=choice.finish_reason,
        model=response.model,
        usage=dict(response.usage),
    )
