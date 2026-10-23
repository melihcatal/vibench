from model_client import get_model_client
from model_models import CompletionResponse


def summarize_text(long_text: str) -> CompletionResponse:
    client = get_model_client()
    prompt = f"Please summarize the following text:\n\n{long_text}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    summary = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason
    return CompletionResponse(text=summary, finish_reason=finish_reason)
