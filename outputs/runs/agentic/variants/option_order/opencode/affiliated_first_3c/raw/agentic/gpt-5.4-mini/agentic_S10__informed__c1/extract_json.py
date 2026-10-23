from model_client import get_openai_client, model_name
from model_models import ChatResponse, normalize_text


def extract_json(text: str) -> ChatResponse:
    client = get_openai_client()
    completion = client.chat.completions.create(
        model=model_name("extract"),
        messages=[
            {
                "role": "system",
                "content": "Extract structured JSON from the input text. Return only valid JSON.",
            },
            {"role": "user", "content": normalize_text(text)},
        ],
        temperature=0,
    )
    return ChatResponse(
        text=completion.choices[0].message.content or "", raw=completion
    )
