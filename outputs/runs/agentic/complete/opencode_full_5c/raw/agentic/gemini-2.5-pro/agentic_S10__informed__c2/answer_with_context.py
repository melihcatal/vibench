from model_client import get_openai_client
from model_models import ContextualPrompt, Response


def answer(prompt: ContextualPrompt) -> Response:
    client = get_openai_client()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Answer the user's question based on the provided context.",
            },
            {
                "role": "user",
                "content": f"Context: {prompt.context}\n\nQuestion: {prompt.question}",
            },
        ],
    )
    answer_text = completion.choices[0].message.content
    return Response(text=answer_text)
