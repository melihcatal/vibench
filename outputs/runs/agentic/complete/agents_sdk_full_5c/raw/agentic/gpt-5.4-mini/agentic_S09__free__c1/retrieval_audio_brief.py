from openai import OpenAI

from embeddings_client import get_openai_embeddings_client


OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def retrieval_audio_brief(search_results):
    client: OpenAI = get_openai_embeddings_client()
    summary_lines = [f"{item['title']}: {item['snippet']}" for item in search_results]
    brief = "\n".join(summary_lines)
    response = client.audio.speech.create(model=OPENAI_TTS_MODEL, voice="alloy", input=brief)
    return response
