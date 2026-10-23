import io
from openai import OpenAI
from embeddings_client import get_openai_client, OPENAI_API_KEY, OPENAI_API_BASE


TTS_MODEL = "tts-1"
TTS_VOICE = "alloy"
TTS_RESPONSE_FORMAT = "mp3"


def generate_spoken_brief(
    search_results: list, voice: str = TTS_VOICE, model: str = TTS_MODEL
):
    brief_text = format_brief_text(search_results)
    client = get_openai_client()
    try:
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=brief_text,
            response_format=TTS_RESPONSE_FORMAT,
        )
        audio_bytes = response.content
        return audio_bytes
    except Exception as exc:
        raise RuntimeError(f"OpenAI TTS error with model {model}: {exc}") from exc


def format_brief_text(search_results: list) -> str:
    if not search_results:
        return "No search results were found."
    lines = ["Here are the search results:"]
    for i, result in enumerate(search_results[:5], 1):
        text = result.get("text", "")
        score = result.get("score", 0.0)
        lines.append(f"Result {i} (relevance score: {score:.2f}): {text}")
    return " ".join(lines)


def save_audio_to_file(audio_bytes: bytes, filepath: str):
    with open(filepath, "wb") as f:
        f.write(audio_bytes)
