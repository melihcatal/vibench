import os
from typing import Dict, Any
from openai import OpenAI
from model_client import get_openai_client


def platform_brief_audio(content: str, voice: str = "alloy") -> Dict[str, Any]:
    """
    Generate spoken briefings from platform outputs using OpenAI's Text-to-Speech API.
    """
    client = get_openai_client()

    # Available OpenAI TTS voices
    available_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    if voice not in available_voices:
        voice = "alloy"

    try:
        # First, summarize or prepare the content for audio briefing
        summary_prompt = f"""
        Create a concise spoken briefing from the following content.
        Make it natural for audio delivery, with clear pacing and emphasis.
        Keep it under 2 minutes when spoken.
        
        Content:
        {content}
        
        Spoken briefing:
        """

        # Generate optimized text for speech
        text_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are creating text optimized for spoken audio delivery.",
                },
                {"role": "user", "content": summary_prompt},
            ],
            temperature=0.5,
            max_tokens=1000,
        )

        speech_text = text_response.choices[0].message.content

        # Generate audio using OpenAI TTS
        audio_response = client.audio.speech.create(
            model="tts-1", voice=voice, input=speech_text
        )

        # Save audio to file
        audio_filename = f"briefing_{voice}.mp3"
        audio_response.stream_to_file(audio_filename)

        # Get file size
        file_size = (
            os.path.getsize(audio_filename) if os.path.exists(audio_filename) else 0
        )

        audio_metadata = {
            "provider": "openai",
            "tts_model": "tts-1",
            "voice": voice,
            "audio_format": "mp3",
            "file_path": audio_filename,
            "file_size_bytes": file_size,
            "text_length": len(speech_text),
            "usage": {
                "text_generation_tokens": text_response.usage.total_tokens,
                "audio_seconds": len(speech_text)
                / 15,  # Rough estimate: 15 chars per second
            },
        }

        return {
            "original_content": content,
            "speech_text": speech_text,
            "audio_file": audio_filename,
            "metadata": audio_metadata,
            "raw_text_response": text_response,
            "voice_options": available_voices,
        }

    except Exception as e:
        raise Exception(f"Failed to generate audio briefing with OpenAI TTS: {str(e)}")


def list_available_voices() -> Dict[str, Any]:
    """
    List available OpenAI TTS voices and their characteristics.
    """
    voices_info = {
        "alloy": {
            "gender": "neutral",
            "style": "versatile",
            "description": "A clear, neutral voice suitable for most content",
        },
        "echo": {
            "gender": "male",
            "style": "warm",
            "description": "A warm, friendly male voice",
        },
        "fable": {
            "gender": "neutral",
            "style": "narrative",
            "description": "Good for storytelling and narratives",
        },
        "onyx": {
            "gender": "male",
            "style": "authoritative",
            "description": "A deep, authoritative male voice",
        },
        "nova": {
            "gender": "female",
            "style": "expressive",
            "description": "An expressive, clear female voice",
        },
        "shimmer": {
            "gender": "female",
            "style": "bright",
            "description": "A bright, cheerful female voice",
        },
    }

    return {
        "provider": "openai",
        "tts_model": "tts-1",
        "available_voices": voices_info,
        "default_voice": "alloy",
    }
