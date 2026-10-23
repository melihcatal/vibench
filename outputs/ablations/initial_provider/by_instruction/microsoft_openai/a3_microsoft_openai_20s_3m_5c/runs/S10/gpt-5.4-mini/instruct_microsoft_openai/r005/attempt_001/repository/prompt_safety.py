from model_client import get_client, get_model


def check_prompt_safety(prompt: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "Classify the text as safe or unsafe and explain briefly."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""
