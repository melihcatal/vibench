import os
import pathlib
from typing import Union

def save_audio(audio_bytes: bytes, destination: Union[str, pathlib.Path]) -> pathlib.Path:
    """Write synthesized audio bytes to a local file or object storage path.

    Args:
        audio_bytes: Raw audio data (e.g., ogg/opus bytes).
        destination: Filesystem path (str/Path) or cloud URI string.

    Returns:
        The resolved pathlib.Path where the file was written.
    """
    dest_path = pathlib.Path(destination)
    if dest_path.is_dir():
        # If destination is a directory, generate a filename based on timestamp
        timestamp = pathlib.Path(".tmp").joinpath(
            f"{pathlib.Path(__file__).stem}_{int(os.time())}.ogg"
        )
        dest_path = timestamp
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_bytes(audio_bytes)
    return dest_path

if __name__ == "__main__":
    # Example usage: save the previously generated sample audio
    test_audio = b"\"placeholder audio bytes\""
    out_file = save_audio(test_audio, "./output")
    print(f"Audio saved to: {out_file}")
