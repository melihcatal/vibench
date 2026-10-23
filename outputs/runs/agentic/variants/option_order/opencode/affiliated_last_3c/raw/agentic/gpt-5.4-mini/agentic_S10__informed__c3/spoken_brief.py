from model_client import get_client, pick_model


def spoken_brief(text: str) -> str:
    client = get_client()
    model = pick_model("spoken_brief")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Rewrite the text as a brief spoken summary.",
            },
            {"role": "user", "content": text},
        ],
        temperature=0.4,
    )
    return resp.choices[0].message.content or ""
