import os

from openai import OpenAI


def visual_safety_text(labels_text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "user",
                "content": f"Check these visual labels for unsafe, hateful, sexual, or self-harm related text and return a short safety judgment: {labels_text}",
            }
        ],
        max_output_tokens=120,
    )
    return getattr(response, "output_text", "") or ""
