import os
from elevenlabs import ElevenLabs
from elevenlabs.client import ElevenLabs as ElevenLabsClient


def generate_audio_brief(
    retrieved_results: list[dict],
    voice: str = "Rachel",
    model: str = "eleven_multilingual_v2",
    api_key: str = None,
) -> bytes:
    api_key = api_key or os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is not set")
    client = ElevenLabs(api_key=api_key)
    brief_text = _build_brief_text(retrieved_results)
    audio_stream = client.text_to_speech.convert(
        voice_id=_get_voice_id(voice),
        output_format="mp3_44100_128",
        text=brief_text,
        model_id=model,
    )
    audio_bytes = b"".join(chunk for chunk in audio_stream)
    return audio_bytes


def _build_brief_text(results: list[dict]) -> str:
    if not results:
        return "No search results were found."
    parts = ["Here is a summary of the search results."]
    for i, result in enumerate(results[:5], 1):
        doc = result.get("document", "Unknown document")
        score = result.get("similarity", 0.0)
        parts.append(f"Result {i}: {doc} with a relevance score of {score:.2f}.")
    parts.append("End of summary.")
    return " ".join(parts)


def _get_voice_id(voice: str) -> str:
    voice_map = {
        "Rachel": "21m00Tcm4TlvDq8ikWAM",
        "Drew": "29vD33N1CtxCmqQRPOHJ",
        "Clyde": "2EiwWnXFnvU5JabPnv8n",
        "Paul": "5Q0t7uMcjvnagumLfvZi",
        "Domi": "AZnzlk1XvdvUeBnXmlld",
    }
    return voice_map.get(voice, "21m00Tcm4TlvDq8ikWAM")
