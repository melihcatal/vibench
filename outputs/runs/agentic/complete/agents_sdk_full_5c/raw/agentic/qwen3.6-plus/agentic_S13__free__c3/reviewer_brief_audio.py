"""Generate spoken briefs for moderation reviewers using OpenAI TTS."""

import os
from typing import List, Optional

from openai import OpenAI


def generate_reviewer_brief_audio(
    brief_text: str,
    voice: str = "nova",
    model: str = "tts-1",
    output_path: Optional[str] = None,
) -> bytes:
    """Generate a spoken audio brief for moderation reviewers.

    Uses OpenAI's text-to-speech model (tts-1 or tts-1-hd) via api.openai.com to
    convert a moderation brief into an audio file that reviewers can listen to
    instead of reading, improving efficiency during high-volume review sessions.

    Args:
        brief_text: The moderation brief text to convert to speech.
        voice: OpenAI TTS voice (default: nova). Options: alloy, echo, fable, onyx, nova, shimmer.
        model: OpenAI TTS model (default: tts-1). Can also use tts-1-hd for higher quality.
        output_path: Optional path to save the audio file. If None, returns bytes.

    Returns:
        Audio bytes of the spoken brief.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)

    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=brief_text,
    )

    audio_bytes = response.content

    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)

    return audio_bytes


def generate_batch_reviewer_briefs(
    brief_texts: List[str],
    voice: str = "nova",
    model: str = "tts-1",
    output_dir: Optional[str] = None,
) -> List[dict]:
    """Generate spoken audio briefs for a batch of moderation cases.

    Uses OpenAI's tts-1 model on api.openai.com to produce audio for each brief.

    Args:
        brief_texts: List of moderation brief strings.
        voice: OpenAI TTS voice (default: nova).
        model: OpenAI TTS model (default: tts-1).
        output_dir: Optional directory to save audio files.

    Returns:
        List of dicts with 'index', 'audio_bytes', 'model', 'voice', and 'provider'.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)

    results = []
    for idx, text in enumerate(brief_texts):
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
        )
        audio_bytes = response.content

        if output_dir:
            filepath = os.path.join(output_dir, f"brief_{idx}.mp3")
            with open(filepath, "wb") as f:
                f.write(audio_bytes)

        results.append({
            "index": idx,
            "audio_bytes": audio_bytes,
            "model": model,
            "voice": voice,
            "provider": "openai",
            "provider_endpoint": "api.openai.com",
        })

    return results


if __name__ == "__main__":
    sample_brief = (
        "Case 2847: User content was flagged for hate speech with a confidence score of 0.94. "
        "The content included slurs targeting a protected group. Appeal received claiming context "
        "was educational. Recommended action: uphold moderation decision."
    )
    audio = generate_reviewer_brief_audio(sample_brief)
    print(f"Generated audio: {len(audio)} bytes")
