from openai import OpenAI


def image_summary(labels, text_blocks, unsafe):
    client = OpenAI()
    payload = {
        "labels": [getattr(label, "name", str(label)) for label in labels],
        "text": [getattr(block, "text", str(block)) for block in text_blocks],
        "unsafe": unsafe,
    }
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": str(payload)}]
    )
    return response.choices[0].message.content
