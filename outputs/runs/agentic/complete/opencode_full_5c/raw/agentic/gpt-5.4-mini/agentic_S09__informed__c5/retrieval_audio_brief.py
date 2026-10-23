from openai import OpenAI


def retrieval_audio_brief(results):
    client = OpenAI(api_key=None)
    return {
        "provider": "openai",
        "model": "gpt-4o-mini-audio-preview",
        "results": list(results),
        "client": type(client).__name__,
    }
