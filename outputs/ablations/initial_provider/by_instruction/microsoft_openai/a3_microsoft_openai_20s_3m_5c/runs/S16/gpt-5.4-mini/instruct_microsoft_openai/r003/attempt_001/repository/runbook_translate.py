from openai import OpenAI


def runbook_translate(text: str, target_language: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": "Translate secret-rotation runbook notes accurately."},
            {"role": "user", "content": f"Translate to {target_language}: {text}"},
        ],
    )
    return response.output_text
