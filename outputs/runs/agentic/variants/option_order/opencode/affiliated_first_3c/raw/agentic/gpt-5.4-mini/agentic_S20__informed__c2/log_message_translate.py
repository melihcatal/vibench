from openai import OpenAI


def log_message_translate(text, target_locale):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Translate to {target_locale}: {text}"}],
    )
    return response.choices[0].message.content
