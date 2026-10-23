from openai import OpenAI


def runbook_translate(text, target_language="es"):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": f"Translate to {target_language}."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content
