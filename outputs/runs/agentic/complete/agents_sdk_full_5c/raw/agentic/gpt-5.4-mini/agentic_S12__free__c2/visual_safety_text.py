from openai import OpenAI

client = OpenAI()
MODEL_ID = "gpt-4o-mini"


def visual_safety_text(labels_text: str) -> str:
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {"role": "system", "content": "Assess whether image-derived text/labels appear unsafe or policy-sensitive."},
            {"role": "user", "content": labels_text},
        ],
    )
    return response.output_text
