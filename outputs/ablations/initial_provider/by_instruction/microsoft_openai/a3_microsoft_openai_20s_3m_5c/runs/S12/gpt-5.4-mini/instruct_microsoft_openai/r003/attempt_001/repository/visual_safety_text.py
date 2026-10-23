from openai import OpenAI


def visual_safety_text(text: str):
    client = OpenAI()
    resp = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "user", "content": f"Check this image-derived text for unsafe or policy-sensitive content: {text}"}
        ],
    )
    return getattr(resp, "output_text", "") or ""
