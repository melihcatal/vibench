from openai import OpenAI


def image_summary(labels, description: str, text_blocks):
    client = OpenAI()
    prompt = {
        "labels": [getattr(x, "name", str(x)) for x in labels],
        "description": description,
        "text": [getattr(x, "text", str(x)) for x in text_blocks],
    }
    response = client.chat.completions.create(
        model="gpt-4.1-mini", messages=[{"role": "user", "content": str(prompt)}]
    )
    return response.choices[0].message.content
