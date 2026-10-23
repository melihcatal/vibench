import os
import base64
from typing import Dict, Any, Optional
from openai import OpenAI
from model_client import get_openai_client


def generate_spoken_briefing(
    text_content: str, voice: str = "alloy", output_format: str = "mp3"
) -> Dict[str, Any]:
    """Generate spoken briefings from platform outputs using OpenAI's Text-to-Speech API."""
    client = get_openai_client()

    # Available voices in OpenAI TTS
    available_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    if voice not in available_voices:
        voice = "alloy"  # Default voice

    # Available output formats
    format_map = {
        "mp3": "mp3",
        "opus": "opus",
        "aac": "aac",
        "flac": "flac",
        "wav": "wav",
        "pcm": "pcm16",
    }

    response_format = format_map.get(output_format.lower(), "mp3")

    # Generate speech using OpenAI TTS
    response = client.audio.speech.create(
        model="tts-1", voice=voice, input=text_content, response_format=response_format
    )

    # Get audio data
    audio_data = response.content

    # Convert to base64 for easy storage/transmission
    audio_base64 = base64.b64encode(audio_data).decode("utf-8")

    return {
        "audio_data": audio_base64,
        "audio_format": response_format,
        "voice": voice,
        "model": "tts-1",
        "text_length": len(text_content),
        "audio_size_bytes": len(audio_data),
    }


def save_audio_to_file(
    audio_data: bytes, filename: str, output_format: str = "mp3"
) -> str:
    """Save audio data to a file."""
    # Ensure proper file extension
    if not filename.endswith(f".{output_format}"):
        filename = f"{filename}.{output_format}"

    with open(filename, "wb") as f:
        f.write(audio_data)

    return os.path.abspath(filename)


def create_summarized_briefing(
    long_text: str,
    summary_length: str = "short",  # "short", "medium", "detailed"
    voice: str = "alloy",
) -> Dict[str, Any]:
    """Create a summarized audio briefing from long text."""
    client = get_openai_client()

    # First, summarize the text
    summary_prompt = f"""Create a {summary_length} audio-friendly summary of the following text.
    The summary should be concise, clear, and suitable for spoken delivery.
    
    Text to summarize:
    {long_text}
    
    Provide only the summary text."""

    summary_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You create concise, spoken-word friendly summaries.",
            },
            {"role": "user", "content": summary_prompt},
        ],
        temperature=0.5,
        max_tokens=500,
    )

    summary_text = summary_response.choices[0].message.content

    # Generate audio from summary
    audio_result = generate_spoken_briefing(summary_text, voice)

    # Decode base64 audio data
    audio_bytes = base64.b64decode(audio_result["audio_data"])

    return {
        "original_text_length": len(long_text),
        "summary_text": summary_text,
        "summary_length": len(summary_text),
        "audio_info": {
            "format": audio_result["audio_format"],
            "voice": audio_result["voice"],
            "size_bytes": audio_result["audio_size_bytes"],
        },
        "audio_bytes": audio_bytes,
        "model_used": "gpt-4o + tts-1",
        "usage": {
            "summary_tokens": summary_response.usage.total_tokens,
            "tts_chars": len(summary_text),
        },
    }


def get_available_voices() -> List[Dict[str, Any]]:
    """Get available TTS voices with descriptions."""
    return [
        {
            "id": "alloy",
            "description": "Clear, neutral voice suitable for most content",
        },
        {"id": "echo", "description": "Warm, friendly voice"},
        {"id": "fable", "description": "Storytelling voice with character"},
        {"id": "onyx", "description": "Deep, authoritative voice"},
        {"id": "nova", "description": "Bright, cheerful voice"},
        {"id": "shimmer", "description": "Soft, calming voice"},
    ]


def estimate_speech_duration(text: str, words_per_minute: int = 150) -> float:
    """Estimate speech duration in seconds."""
    # Rough estimation: average English word length is 5 characters
    word_count = len(text.split())
    minutes = word_count / words_per_minute
    seconds = minutes * 60
    return seconds


def create_multilingual_briefing(
    text: str, target_language: str, voice: str = "alloy"
) -> Dict[str, Any]:
    """Create audio briefing in another language."""
    from localized_platform_output import translate_platform_output

    # Translate the text
    translated_text = translate_platform_output(text, target_language)

    # Generate audio in translated language
    # Note: OpenAI TTS primarily supports English, but we'll attempt anyway
    audio_result = generate_spoken_briefing(translated_text, voice)

    audio_bytes = base64.b64decode(audio_result["audio_data"])

    return {
        "original_text": text,
        "translated_text": translated_text,
        "target_language": target_language,
        "audio_bytes": audio_bytes,
        "audio_format": audio_result["audio_format"],
        "voice": voice,
        "estimated_duration_seconds": estimate_speech_duration(translated_text),
    }


if __name__ == "__main__":
    # Example usage
    briefing_text = """Good morning team. Here's your daily briefing.
    Project Alpha is on track for Friday's deadline. 
    The new feature deployment completed successfully overnight.
    Customer feedback has been positive, with a 95% satisfaction rate.
    Remember the all-hands meeting at 2 PM today in the main conference room."""

    # Generate basic audio briefing
    audio_result = generate_spoken_briefing(briefing_text, voice="nova")
    print(f"Audio generated: {audio_result['audio_size_bytes']} bytes")
    print(f"Format: {audio_result['audio_format']}")
    print(f"Voice: {audio_result['voice']}")

    # Create summarized briefing
    long_text = """The quarterly financial report shows strong growth across all sectors. 
    Revenue increased by 15% compared to last quarter, exceeding projections by 3%. 
    The European market showed particularly strong performance with 22% growth. 
    Operational costs remained stable, leading to improved profit margins. 
    The board has approved the expansion plan for Q3, focusing on Asian markets."""

    summarized = create_summarized_briefing(long_text, summary_length="short")
    print(f"\nSummarized briefing created:")
    print(f"Original: {summarized['original_text_length']} chars")
    print(f"Summary: {summarized['summary_length']} chars")
    print(f"Audio size: {summarized['audio_info']['size_bytes']} bytes")

    # Get available voices
    voices = get_available_voices()
    print(f"\nAvailable voices: {[v['id'] for v in voices]}")
