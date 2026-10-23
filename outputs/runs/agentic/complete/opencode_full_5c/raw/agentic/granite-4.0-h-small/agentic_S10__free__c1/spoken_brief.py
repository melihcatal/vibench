import json
import os
import tempfile
import subprocess
from model_client import create_client
from model_models import normalize


def generate_spoken_brief(text: str, model: str = "gpt-4o-mini") -> bytes:
    """Generate a short spoken brief (audio) from model output.

    This function uses the hosted LLM to produce a concise transcript and then
    invokes a TTS service (e.g., Google Cloud Text-to-Speech) to return audio
    bytes. Adjust the TTS client for your chosen provider.
    """
    # 1) Summarize to a brief transcript using the LLM
    summary = summarize_text(text, model=model)

    # 2) Call external TTS (example using gcloud CLI; replace with your provider's SDK)
    # Ensure gcloud is authenticated and the TTS component is installed.
    # Create temporary file for input text
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tmp_in:
        tmp_in.write(summary)
        in_path = tmp_in.name

    # Generate audio; change --voice, --audio-encoding as needed
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".mp3") as tmp_out:
        out_path = tmp_out.name

    cmd = [
        "gcloud",
        "text-to-speech",
        "synthesize",
        f"--text='@{in_path}'",
        f"--voice='en-US-Standard-C'",  # adjust voice
        f"--audio-encoding=MP3",
        f"--output-file='{out_path}'",
    ]
    subprocess.run(cmd, check=True)

    # Read back audio bytes
    with open(out_path, "rb") as f:
        audio_bytes = f.read()

    # Cleanup temporary files
    os.remove(in_path)
    os.remove(out_path)

    return audio_bytes
