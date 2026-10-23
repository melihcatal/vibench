from openai import OpenAI


def live_caption_translate(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key"))
    target_language = payload.get("target_language", "es")
    text = payload.get("text", "")
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": f"Translate live captions into {target_language}."},
            {"role": "user", "content": text},
        ],
    )
    return {"translation": response.choices[0].message.content}
