from openai import OpenAI

from model_client import get_client, pick_model


def check_prompt_safety(text: str) -> bool:
    client: OpenAI = get_client()
    model = pick_model("safety")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Assess whether the text is unsafe. Reply with SAFE or UNSAFE.",
            },
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    return (resp.choices[0].message.content or "").strip().upper().startswith("SAFE")
