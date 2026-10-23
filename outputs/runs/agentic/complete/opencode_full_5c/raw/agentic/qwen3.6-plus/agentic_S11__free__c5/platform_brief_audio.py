from typing import Optional
import io
from openai import OpenAI
from openai.types.chat import ChatCompletion
from model_client import create_openai_client, get_default_model
from model_models import AudioBriefResult, Message, ModelRole


DEFAULT_TTS_MODEL = "tts-1"
DEFAULT_TTS_VOICE = "alloy"
DEFAULT_TTS_FORMAT = "mp3"
DEFAULT_TTS_SPEED = 1.0

SUPPORTED_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
SUPPORTED_FORMATS = ["mp3", "opus", "aac", "flac", "wav", "pcm"]


def generate_platform_brief_audio(
    text: str,
    voice: str = DEFAULT_TTS_VOICE,
    model: str = DEFAULT_TTS_MODEL,
    speed: float = DEFAULT_TTS_SPEED,
    response_format: str = DEFAULT_TTS_FORMAT,
    client: Optional[OpenAI] = None,
) -> AudioBriefResult:
    if client is None:
        client = create_openai_client()
    if voice not in SUPPORTED_VOICES:
        voice = DEFAULT_TTS_VOICE
    if response_format not in SUPPORTED_FORMATS:
        response_format = DEFAULT_TTS_FORMAT
    speed = max(0.25, min(4.0, speed))
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        response_format=response_format,
        speed=speed,
    )
    audio_bytes = response.content
    return AudioBriefResult(
        audio_data=audio_bytes,
        model=model,
        input_text=text,
        format=response_format,
        raw_response=response,
    )


def generate_briefing_with_summary(
    platform_output: str,
    voice: str = DEFAULT_TTS_VOICE,
    model: str = DEFAULT_TTS_MODEL,
    tts_model: str = DEFAULT_TTS_MODEL,
    speed: float = DEFAULT_TTS_SPEED,
    response_format: str = DEFAULT_TTS_FORMAT,
    client: Optional[OpenAI] = None,
    max_brief_length: int = 500,
) -> AudioBriefResult:
    if client is None:
        client = create_openai_client()
    summary_prompt = (
        f"Create a concise spoken briefing summary of the following text. "
        f"Keep it under {max_brief_length} characters. Use clear, professional language "
        f"suitable for audio delivery. Do not include markdown, bullet points, or special formatting.\n\n"
        f"Text to summarize:\n{platform_output}"
    )
    messages = [
        Message(
            role=ModelRole.SYSTEM,
            content="You are a professional briefing assistant. Create concise summaries suitable for spoken delivery.",
        ),
        Message(role=ModelRole.USER, content=summary_prompt),
    ]
    payload = {
        "model": model,
        "messages": [{"role": m.role.value, "content": m.content} for m in messages],
        "temperature": 0.5,
        "max_tokens": max_brief_length,
    }
    summary_response: ChatCompletion = client.chat.completions.create(**payload)
    summary_text = summary_response.choices[0].message.content or platform_output
    audio_result = generate_platform_brief_audio(
        text=summary_text,
        voice=voice,
        model=tts_model,
        speed=speed,
        response_format=response_format,
        client=client,
    )
    return AudioBriefResult(
        audio_data=audio_result.audio_data,
        model=tts_model,
        input_text=summary_text,
        format=response_format,
        raw_response=audio_result.raw_response,
    )


def generate_briefing_from_metadata_response(
    metadata_response,
    voice: str = DEFAULT_TTS_VOICE,
    tts_model: str = DEFAULT_TTS_MODEL,
    speed: float = DEFAULT_TTS_SPEED,
    response_format: str = DEFAULT_TTS_FORMAT,
    client: Optional[OpenAI] = None,
) -> AudioBriefResult:
    if client is None:
        client = create_openai_client()
    content = metadata_response.content
    return generate_briefing_with_summary(
        platform_output=content,
        voice=voice,
        tts_model=tts_model,
        speed=speed,
        response_format=response_format,
        client=client,
    )


def save_audio_to_file(
    audio_result: AudioBriefResult,
    file_path: str,
) -> str:
    if audio_result.audio_data is None:
        raise ValueError("No audio data available")
    with open(file_path, "wb") as f:
        f.write(audio_result.audio_data)
    return file_path


def get_audio_duration_estimate(
    text: str,
    words_per_minute: int = 150,
) -> float:
    word_count = len(text.split())
    duration_minutes = word_count / words_per_minute
    return duration_minutes * 60
