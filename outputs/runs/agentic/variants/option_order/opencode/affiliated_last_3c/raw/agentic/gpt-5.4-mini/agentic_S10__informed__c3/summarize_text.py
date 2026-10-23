from model_client import get_client, pick_model


def summarize_text(text: str) -> str:
    client = get_client()
    model = pick_model("summarize")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Summarize the user's text concisely."},
            {"role": "user", "content": text},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content or ""
