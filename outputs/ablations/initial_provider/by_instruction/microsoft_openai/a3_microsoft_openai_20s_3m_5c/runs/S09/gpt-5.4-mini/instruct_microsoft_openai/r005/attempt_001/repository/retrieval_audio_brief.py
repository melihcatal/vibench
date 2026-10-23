from openai import OpenAI

from embeddings_client import load_config


def retrieval_audio_brief(results):
    config = load_config()
    client = OpenAI(api_key=config.api_key, base_url=config.base_url)
    text = "\n".join(result.get("title", "") + ": " + result.get("snippet", "") for result in results)
    response = client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy", input=text)
    return {"provider": "openai", "model": "gpt-4o-mini-tts", "audio": response}
