from model_client import get_openai_client
from model_models import ModelResponse


def summarize_text(text_to_summarize: str) -> ModelResponse:
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text.",
            },
            {
                "role": "user",
                "content": f"Please summarize the following text:\n\n{text_to_summarize}",
            },
        ],
        max_tokens=150,
        temperature=0.7,
    )
    choice = response.choices[0]
    return ModelResponse(
        text=choice.message.content,
        finish_reason=choice.finish_reason,
        model=response.model,
        usage=dict(response.usage),
    )
