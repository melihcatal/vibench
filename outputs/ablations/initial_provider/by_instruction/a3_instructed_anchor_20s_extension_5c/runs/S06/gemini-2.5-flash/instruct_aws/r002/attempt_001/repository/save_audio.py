from typing import BinaryIO

def save_audio_to_file(audio_stream: BinaryIO, output_filepath: str):
    """
    Saves an audio byte stream to a local file.
    """
    try:
        with open(output_filepath, "wb") as f:
            f.write(audio_stream.read())
        print(f"Audio successfully saved to {output_filepath}")
    except Exception as e:
        print(f"Error saving audio to file: {e}")
