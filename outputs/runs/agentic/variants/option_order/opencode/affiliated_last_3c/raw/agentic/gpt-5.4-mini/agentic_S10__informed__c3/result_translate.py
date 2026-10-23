from model_client import get_client, pick_model


def result_translate(text: str, target_language: str) -> str:
    client = get_client()
    model = pick_model("translate")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"Translate the user's text into {target_language}.",
            },
            {"role": "user", "content": text},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content or ""
