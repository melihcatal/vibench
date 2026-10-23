from model_client import create_client, model_name


def summarize_text(text: str) -> str:
    client = create_client()
    response = client.chat.completions.create(
        model=model_name(),
        messages=[
            {"role": "system", "content": "Summarize the provided text clearly and concisely."},
            {"role": "user", "content": text},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content
