from openai import OpenAI


def alt_text_translate(text: str, target_language: str):
    client = OpenAI()
    resp = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "user",
                "content": f"Translate this image alt text into {target_language}: {text}",
            }
        ],
    )
    return getattr(resp, "output_text", "") or ""
