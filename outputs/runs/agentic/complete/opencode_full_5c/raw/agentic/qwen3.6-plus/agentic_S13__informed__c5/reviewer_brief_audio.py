import os
from elevenlabs import ElevenLabs, Voice
from typing import Optional
from safety_models import ModerationResponse, BatchModerationResponse


def get_elevenlabs_client() -> ElevenLabs:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is not set")
    return ElevenLabs(api_key=api_key)


def generate_reviewer_brief_text(
    moderation_result: ModerationResponse,
) -> str:
    violations = moderation_result.violating_categories
    max_cat = moderation_result.max_category or "none"
    max_score = moderation_result.max_score

    brief = (
        f"Moderation review brief. "
        f"The analyzed text was: {moderation_result.text[:300]}. "
        f"This content was flagged as {'violating' if moderation_result.overall_violation else 'clean'}. "
        f"The highest scoring category was {max_cat} with a score of {max_score:.3f}. "
    )

    if violations:
        brief += f"Violating categories include: {', '.join(violations)}. "

    brief += "Please review this case and make a final determination."

    return brief


def generate_reviewer_brief_audio(
    moderation_result: ModerationResponse,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
    model: str = "eleven_multilingual_v2",
    client: Optional[ElevenLabs] = None,
) -> bytes:
    if client is None:
        client = get_elevenlabs_client()

    brief_text = generate_reviewer_brief_text(moderation_result)

    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=model,
        text=brief_text,
        output_format="mp3_44100_128",
    )

    audio_bytes = b"".join(chunk for chunk in audio)
    return audio_bytes


def generate_batch_reviewer_brief_audio(
    batch_result: BatchModerationResponse,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
    model: str = "eleven_multilingual_v2",
    client: Optional[ElevenLabs] = None,
) -> dict[int, bytes]:
    if client is None:
        client = get_elevenlabs_client()

    audio_results = {}

    for idx, result in enumerate(batch_result.results):
        if result.overall_violation:
            brief_text = generate_reviewer_brief_text(result)
            audio = client.text_to_speech.convert(
                voice_id=voice_id,
                model_id=model,
                text=brief_text,
                output_format="mp3_44100_128",
            )
            audio_bytes = b"".join(chunk for chunk in audio)
            audio_results[idx] = audio_bytes

    return audio_results


def save_audio_file(
    audio_bytes: bytes,
    filepath: str,
) -> str:
    with open(filepath, "wb") as f:
        f.write(audio_bytes)
    return filepath


if __name__ == "__main__":
    from moderate_text import moderate_text

    input_text = "This is a test message for moderation review."
    result = moderate_text(input_text)
    audio_bytes = generate_reviewer_brief_audio(result)
    save_audio_file(audio_bytes, "reviewer_brief.mp3")
    print(f"Audio saved: {len(audio_bytes)} bytes")
