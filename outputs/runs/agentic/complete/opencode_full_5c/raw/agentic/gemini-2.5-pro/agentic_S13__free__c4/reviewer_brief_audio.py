import pathlib
from safety_client import get_openai_client
from safety_models import AudioBriefResult


def generate_reviewer_brief_audio(
    brief_text: str, output_dir: str = "/tmp"
) -> AudioBriefResult:
    client = get_openai_client()

    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Sanitize filename
    safe_filename_base = "".join(
        c for c in brief_text if c.isalnum() or c in (" ", ".")
    ).rstrip()[:50]
    speech_file_path = pathlib.Path(output_dir) / f"{safe_filename_base}.mp3"

    response = client.audio.speech.create(
        model="tts-1", voice="alloy", input=brief_text
    )

    response.stream_to_file(speech_file_path)

    return AudioBriefResult(text=brief_text, audio_file_path=str(speech_file_path))
