from safety_client import elevenlabs_client

def reviewer_brief_audio(brief_text: str, output_file: str = "reviewer_brief.mp3", voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> str:
    client = elevenlabs_client()
    audio = client.text_to_speech.convert(
        text=brief_text,
        voice_id=voice_id,
        model_id="eleven_monolingual_v1",
        output_format="mp3_44100_128"
    )
    with open(output_file, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    return output_file