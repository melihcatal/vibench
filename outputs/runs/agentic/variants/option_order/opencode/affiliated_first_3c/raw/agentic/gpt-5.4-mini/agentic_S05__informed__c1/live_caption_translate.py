from openai import OpenAI


def live_caption_translate(text: str, target_language: str = "es"):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Translate live captions into the target language.",
            },
            {"role": "user", "content": f"Translate to {target_language}: {text}"},
        ],
    )
    return response.choices[0].message.content
