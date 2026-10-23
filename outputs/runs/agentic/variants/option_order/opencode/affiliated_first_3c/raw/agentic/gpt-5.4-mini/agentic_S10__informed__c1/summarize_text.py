from model_client import get_openai_client, model_name
from model_models import ChatResponse, normalize_text


def summarize_text(text: str) -> ChatResponse:
    client = get_openai_client()
    completion = client.chat.completions.create(
        model=model_name("summary"),
        messages=[
            {
                "role": "system",
                "content": "Summarize the given text clearly and concisely.",
            },
            {"role": "user", "content": normalize_text(text)},
        ],
        temperature=0.2,
    )
    return ChatResponse(
        text=completion.choices[0].message.content or "", raw=completion
    )
