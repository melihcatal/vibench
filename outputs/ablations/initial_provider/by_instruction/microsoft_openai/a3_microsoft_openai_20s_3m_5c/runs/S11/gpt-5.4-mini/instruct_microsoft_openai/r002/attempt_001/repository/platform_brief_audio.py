from model_client import create_platform_client, load_platform_config


def platform_brief_audio(text: str) -> bytes:
    config = load_platform_config()
    client = create_platform_client(config)
    result = client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy", input=text)
    return result.read()
