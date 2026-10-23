from openai import OpenAI


def image_summary(labels, text_blocks=None, safety=None):
    client = OpenAI()
    prompt = {
        "labels": labels,
        "text_blocks": text_blocks or [],
        "safety": safety or {},
    }
    response = client.chat.completions.create(
        model="gpt-5.4-mini", messages=[{"role": "user", "content": str(prompt)}]
    )
    return response.choices[0].message.content
