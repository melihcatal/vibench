from pathlib import Path

from synthesize_text import synthesize_text


def save_audio(text, destination, voice_id=None, output_format=None, engine=None):
    audio = synthesize_text(text, voice_id=voice_id, output_format=output_format, engine=engine)
    if hasattr(destination, "write"):
        destination.write(audio)
        return destination
    path = Path(destination)
    path.write_bytes(audio)
    return str(path)
