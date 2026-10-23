import os
import json
import requests
import wave
import tempfile

# AssemblyAI transcription API (example provider)
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
TRANSCRIBE_ENDPOINT = "https://api.assemblyai.com/v2/transcript"


def transcribe_qa_audio(audio_bytes: bytes) -> Dict[str, Any]:
    """Transcribe synthesized QA audio to text using AssemblyAI.

    Args:
        audio_bytes: RAW PCM (16‑bit mono) bytes produced by TTS.

    Returns:
        JSON response containing transcription result.
    """
    # Upload audio to a temporary location
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        audio_path = tmp.name
    # Submit transcription request
    headers = {
        "Authorization": ASSEMBLYAI_API_KEY,
        "Content-Type": "multipart/form-data",
    }
    files = {
        "audio": (os.path.basename(audio_path), open(audio_path, "rb"), "audio/wav")
    }
    resp = requests.post(TRANSCRIBE_ENDPOINT, headers=headers, files=files)
    resp.raise_for_status()
    transcript_id = resp.json().get("id")
    # Poll until transcription is complete (simple sync loop)
    while True:
        poll_resp = requests.get(
            f"{TRANSCRIBE_ENDPOINT}/{transcript_id}",
            headers={"Authorization": ASSEMBLYAI_API_KEY},
        )
        poll_resp.raise_for_status()
        status = poll_resp.json().get("status")
        if status == "completed":
            return poll_resp.json()
        if status == "error":
            raise RuntimeError("Transcription failed")
        # wait a moment before polling again
        import time

        time.sleep(1)
    # teardown temporary file (optional)
    os.unlink(audio_path)


# Example usage (remove in production)
if __name__ == "__main__":
    # Generate a tiny test audio (sine wave) – replace with real TTS output
    import numpy as np

    sample_rate = 16000
    secs = 2
    t = np.linspace(0, secs, int(sample_rate * secs), endpoint=False)
    audio = np.int16(32767 * np.sin(2 * np.pi * 440 * t))  # 440 Hz tone
    transcript = transcribe_qa_audio(audio)
    print(transcript)
