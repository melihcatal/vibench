import os
from typing import Dict, Any
from openai import OpenAI


def platform_brief_audio(
    text: str, voice: str = "alloy", output_format: str = "mp3"
) -> Dict[str, Any]:
    """
    Generate spoken briefings from platform outputs using OpenAI's Text-to-Speech API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Validate voice parameter
    valid_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    if voice not in valid_voices:
        voice = "alloy"

    # Validate output format
    valid_formats = ["mp3", "opus", "aac", "flac", "wav", "pcm"]
    if output_format not in valid_formats:
        output_format = "mp3"

    # Generate speech audio
    response = client.audio.speech.create(
        model="tts-1", voice=voice, input=text, response_format=output_format
    )

    # Save audio to file
    output_filename = f"briefing_{voice}.{output_format}"
    response.stream_to_file(output_filename)

    # Get file size
    file_size = os.path.getsize(output_filename)

    # Estimate audio duration (rough estimate: 150 words per minute)
    word_count = len(text.split())
    estimated_duration_seconds = (word_count / 150) * 60

    # Create metadata about the audio generation
    audio_metadata = {
        "text": text,
        "voice": voice,
        "output_format": output_format,
        "output_filename": output_filename,
        "file_size_bytes": file_size,
        "estimated_duration_seconds": estimated_duration_seconds,
        "word_count": word_count,
        "tts_model": "tts-1",
        "character_count": len(text),
    }

    # Generate a brief transcript summary using GPT
    try:
        summary_prompt = f"""Create a brief summary of this audio transcript for metadata purposes:
        
        {text}
        
        Provide a 1-2 sentence summary."""

        summary_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You create concise summaries of audio transcripts.",
                },
                {"role": "user", "content": summary_prompt},
            ],
            max_tokens=100,
            temperature=0.3,
        )

        audio_metadata["summary"] = summary_response.choices[0].message.content
        audio_metadata["summary_usage"] = {
            "prompt_tokens": summary_response.usage.prompt_tokens,
            "completion_tokens": summary_response.usage.completion_tokens,
            "total_tokens": summary_response.usage.total_tokens,
        }
    except Exception as e:
        audio_metadata["summary"] = f"Summary generation failed: {str(e)}"

    return audio_metadata
