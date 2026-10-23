import os

from openai import OpenAI


def runbook_translate(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key") or os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": f'Translate this secret-rotation runbook note to {payload["target_language"]}: {payload["text"]}',
            }
        ],
    )
    return {"translation": response.output_text}
