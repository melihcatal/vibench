from model_client import get_client, pick_model


def spoken_brief(text, model=None):
    client = get_client()
    response = client.chat.completions.create(
        model=pick_model(model),
        messages=[
            {"role": "system", "content": "Rewrite the text as a short spoken brief."},
            {"role": "user", "content": text},
        ],
        temperature=0.3,
        max_tokens=180,
    )
    return response.choices[0].message.content
