from openai import OpenAI


def localized_audio_preview(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=payload.get("voice", "alloy"),
        input=payload["text"],
    )
    return {"audio": response}
