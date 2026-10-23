from openai import OpenAI


def metric_annotation_safety(text: str):
    client = OpenAI()
    return client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Check free-text metric labels or annotations for unsafe text."},
            {"role": "user", "content": text},
        ],
    )
