import os


def save_audio_to_file(audio_content: bytes, file_path: str):
    """Writes synthesized speech audio to a local file.

    Args:
        audio_content: The audio content as a byte string.
        file_path: The full path to the file where the audio should be saved.
    """
    # Ensure the directory exists
    output_dir = os.path.dirname(file_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(file_path, "wb") as out:
        out.write(audio_content)
    print(f"Audio content written to file: {file_path}")
