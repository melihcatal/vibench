from openai import OpenAI


def retrieval_audio_brief(results):
    client = OpenAI()
    return {"provider": "openai", "brief": "; ".join(str(item) for item in results)}
