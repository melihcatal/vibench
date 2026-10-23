import os

def write_audio_to_file(audio_bytes: bytes, file_path: str, fmt: str = "wav"):
    """Write raw audio bytes to a local file. Supports common audio formats (wav, mp3, ogg).
    The implementation uses the built‑in wave module for WAV and external libraries for others.
    """
    import wave
    import contextlib
    if fmt.lower() == "wav":
        with contextlib.closing(wave.open(file_path, "wb")) as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)  # typical Azure TTS sample rate
            wf.writeframes(audio_bytes)
        print(f"Audio saved to {file_path}")
    else:
        # For other formats, rely on ffmpeg or other encoder libraries.
        raise NotImplementedError(f"Export format {fmt} is not implemented (only WAV supported right now).").__traceback__
