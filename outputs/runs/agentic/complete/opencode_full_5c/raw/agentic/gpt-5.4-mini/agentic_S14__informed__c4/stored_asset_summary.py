from openai import OpenAI


def stored_asset_summary(text: str, model: str = "gpt-5.4-mini") -> str:
    client = OpenAI()
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": f"Summarize this asset content:\n{text}"}
        ],
    )
    return resp.choices[0].message.content or ""
