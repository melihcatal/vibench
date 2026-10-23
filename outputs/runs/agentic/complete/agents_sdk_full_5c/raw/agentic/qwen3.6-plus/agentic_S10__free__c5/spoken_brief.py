"""
spoken_brief.py - Generate a spoken brief from the model output.

Uses OpenAI's Chat Completions API with gpt-4o to generate a speech-friendly brief,
and OpenAI's Text-to-Speech API (tts-1 model) for audio synthesis.
"""

import io
from typing import Optional

from model_client import get_openai_client, select_model, build_chat_messages


OPENAI_TTS_MODEL_STANDARD = "tts-1"
OPENAI_TTS_MODEL_HD = "tts-1-hd"
OPENAI_TTS_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
OPENAI_TTS_ENDPOINT = "https://api.openai.com/v1/audio/speech"


def generate_brief_script(
    text: str,
    target_duration_seconds: int = 30,
    tone: str = "professional",
    model_family: str = "gpt-4o",
) -> str:
    """
    Convert model output into a concise, speech-friendly brief script
    using OpenAI's hosted LLM.

    Args:
        text: The original text output from the model.
        target_duration_seconds: Target spoken duration in seconds.
        tone: Desired tone (e.g. "professional", "casual", "urgent").
        model_family: OpenAI model family for script generation.

    Returns:
        A plain-text brief script optimized for spoken delivery.
    """
    client = get_openai_client()
    model_id = select_model(model_family)

    words_per_minute = 150
    target_words = int((target_duration_seconds / 60.0) * words_per_minute)

    system_prompt = (
        "You are a broadcast scriptwriter. Convert provided text into a "
        f"concise spoken brief of approximately {target_words} words. "
        f"Use a {tone} tone. Write naturally for speech: short sentences, "
        "clear transitions, and conversational phrasing. "
        "Avoid markdown, headers, or formatting. Return ONLY the script text."
    )

    user_content = (
        f"Convert the following into a spoken brief:\n\n{text}"
    )

    messages = build_chat_messages(
        system_prompt=system_prompt,
        user_content=user_content,
    )

    completion = client.chat.completions.create(
        model=model_id,
        messages=messages,
        temperature=0.5,
        max_tokens=512,
    )

    script = ""
    if completion.choices and completion.choices[0].message:
        script = completion.choices[0].message.content or ""

    return script.strip()


def synthesize_speech(
    text: str,
    voice: str = "alloy",
    model: str = OPENAI_TTS_MODEL_STANDARD,
    response_format: str = "mp3",
    speed: float = 1.0,
) -> bytes:
    """
    Convert the brief script to audio using OpenAI's Text-to-Speech API.

    Args:
        text: The text to synthesize.
        voice: OpenAI TTS voice name (alloy, echo, fable, onyx, nova, shimmer).
        model: OpenAI TTS model ID (tts-1 or tts-1-hd).
        response_format: Audio format (mp3, opus, aac, flac).
        speed: Playback speed multiplier (0.25 to 4.0).

    Returns:
        Raw audio bytes in the requested format.
    """
    client = get_openai_client()

    if voice not in OPENAI_TTS_VOICES:
        raise ValueError(f"Invalid voice '{voice}'. Choose from: {OPENAI_TTS_VOICES}")

    speed = max(0.25, min(4.0, speed))

    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        response_format=response_format,
        speed=speed,
    )

    return response.content


def generate_spoken_brief(
    text: str,
    target_duration_seconds: int = 30,
    tone: str = "professional",
    voice: str = "nova",
    tts_model: str = OPENAI_TTS_MODEL_STANDARD,
    llm_model_family: str = "gpt-4o",
) -> tuple[str, bytes]:
    """
    Full pipeline: generate a spoken brief script and synthesize audio.

    Args:
        text: The original model output text.
        target_duration_seconds: Target duration for the brief.
        tone: Desired tone for the script.
        voice: OpenAI TTS voice to use.
        tts_model: OpenAI TTS model (tts-1 or tts-1-hd).
        llm_model_family: OpenAI LLM model family for script generation.

    Returns:
        Tuple of (brief_script, audio_bytes).
    """
    script = generate_brief_script(
        text=text,
        target_duration_seconds=target_duration_seconds,
        tone=tone,
        model_family=llm_model_family,
    )

    audio = synthesize_speech(
        text=script,
        voice=voice,
        model=tts_model,
    )

    return script, audio


def save_audio(audio_bytes: bytes, output_path: str) -> str:
    """
    Save synthesized audio bytes to a file.

    Args:
        audio_bytes: Raw audio data from OpenAI TTS.
        output_path: File path to save the audio.

    Returns:
        The output file path.
    """
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    return output_path


if __name__ == "__main__":
    sample_text = (
        "Quarterly earnings report: Revenue increased 15% year-over-year to $4.2 billion. "
        "Net income rose 22% to $890 million. Cloud services division grew 35%, "
        "driven by enterprise adoption of AI-powered tools. The company raised its "
        "full-year guidance and announced a new $5 billion share buyback program."
    )

    print("Generating spoken brief with OpenAI gpt-4o and tts-1...")
    script, audio = generate_spoken_brief(
        text=sample_text,
        target_duration_seconds=20,
        tone="professional",
        voice="nova",
        tts_model=OPENAI_TTS_MODEL_STANDARD,
    )

    print(f"\nScript:\n{script}")
    print(f"Audio size: {len(audio)} bytes")
